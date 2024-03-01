from functools import reduce
from itertools import cycle
from math import factorial
from scipy.ndimage import map_coordinates, spline_filter
from scipy.sparse.linalg import factorized
from PIL import Image
from scipy.special import erf

import numpy as np
import scipy.sparse as sp

# modified from GregTJ's Stable Fluids project
# https://github.com/GregTJ/stable-fluids
# Unlicense license

#region FluidSim class

class FluidSimGif():
    def __init__(self, size_x, size_y, duration, 
                 inflow_padding=50, inflow_duration=60, inflow_radius=8, inflow_velo=1, inflow_count=5):
        self.resolution = size_y, size_x
        self.duration = duration
        self.inflow_duration = inflow_duration

        print('Generating fluid solver, this may take some time.')
        self.fluid = Fluid(self.resolution, 'dye')

        center = np.floor_divide(self.resolution, 2)
        r = np.min(center) - inflow_padding

        points = np.linspace(-np.pi, np.pi, inflow_count, endpoint=False)
        points = tuple(np.array((np.cos(p), np.sin(p))) for p in points)
        normals = tuple(-p for p in points)
        points = tuple(r * p + center for p in points)

        self.inflow_velocity = np.zeros_like(self.fluid.velocity)
        self.inflow_dye = np.zeros(self.fluid.shape)
        for p, n in zip(points, normals):
            mask = np.linalg.norm(self.fluid.indices - p[:, None, None], axis=0) <= inflow_radius
            self.inflow_velocity[:, mask] += n[:, None] * inflow_velo
            self.inflow_dye[mask] = 1

    def main(self):
        frames = []
        for f in range(self.duration):
            print(f'Computing frame {f + 1} of {self.duration}.')
            if f <= self.inflow_duration:
                self.fluid.velocity += self.inflow_velocity
                self.fluid.dye += self.inflow_dye

            curl = self.fluid.step()[1]
            # Using the error function to make the contrast a bit higher. 
            # Any other sigmoid function e.g. smoothstep would work.
            curl = (erf(curl * 2) + 1) / 4

            color = np.dstack((curl, np.ones(self.fluid.shape), self.fluid.dye))
            color = (np.clip(color, 0, 1) * 255).astype('uint8')
            frames.append(Image.fromarray(color, mode='HSV').convert('RGB'))

        print('Saving simulation result.')
        frames[0].save('example.gif', save_all=True, append_images=frames[1:], duration=20, loop=0)

#endregion

#region Fluid Class

class Fluid:
    def __init__(self, shape, *quantities, pressure_order=1, advect_order=3):
        self.shape = shape
        self.dimensions = len(shape)

        # Prototyping is simplified by dynamically 
        # creating advected quantities as needed.
        self.quantities = quantities
        for q in quantities:
            setattr(self, q, np.zeros(shape))

        self.indices = np.indices(shape)
        self.velocity = np.zeros((self.dimensions, *shape))

        laplacian = operator(shape, difference(2, pressure_order))
        self.pressure_solver = factorized(laplacian)
        
        self.advect_order = advect_order

    def step(self):
        # Advection is computed backwards in time as described in Stable Fluids.
        advection_map = self.indices - self.velocity

        # SciPy's spline filter introduces checkerboard divergence.
        # A linear blend of the filtered and unfiltered fields based
        # on some value epsilon eliminates this error.
        def advect(field, filter_epsilon=10e-2, mode='constant'):
            filtered = spline_filter(field, order=self.advect_order, mode=mode)
            field = filtered * (1 - filter_epsilon) + field * filter_epsilon
            return map_coordinates(field, advection_map, prefilter=False, order=self.advect_order, mode=mode)

        # Apply advection to each axis of the
        # velocity field and each user-defined quantity.
        for d in range(self.dimensions):
            self.velocity[d] = advect(self.velocity[d])

        for q in self.quantities:
            setattr(self, q, advect(getattr(self, q)))

        # Compute the jacobian at each point in the
        # velocity field to extract curl and divergence.
        jacobian_shape = (self.dimensions,) * 2
        partials = tuple(np.gradient(d) for d in self.velocity)
        jacobian = np.stack(partials).reshape(*jacobian_shape, *self.shape)

        divergence = jacobian.trace()

        # If this curl calculation is extended to 3D, the y-axis value must be negated.
        # This corresponds to the coefficients of the levi-civita symbol in that dimension.
        # Higher dimensions do not have a vector -> scalar, or vector -> vector,
        # correspondence between velocity and curl due to differing isomorphisms
        # between exterior powers in dimensions != 2 or 3 respectively.
        curl_mask = np.triu(np.ones(jacobian_shape, dtype=bool), k=1)
        curl = (jacobian[curl_mask] - jacobian[curl_mask.T]).squeeze()

        # Apply the pressure correction to the fluid's velocity field.
        pressure = self.pressure_solver(divergence.flatten()).reshape(self.shape)
        self.velocity -= np.gradient(pressure)

        return divergence, curl, pressure
    
#endregion

#region Helper Functions

def difference(derivative, accuracy=1):
    # Central differences implemented based on the article here:
    # http://web.media.mit.edu/~crtaylor/calculator.html
    derivative += 1
    radius = accuracy + derivative // 2 - 1
    points = range(-radius, radius + 1)
    coefficients = np.linalg.inv(np.vander(points))
    return coefficients[-derivative] * factorial(derivative - 1), points


def operator(shape, *differences):
    # Credit to Philip Zucker for figuring out
    # that kronsum's argument order is reversed.
    # Without that bit of wisdom I'd have lost it.
    differences = zip(shape, cycle(differences))
    factors = (sp.diags(*diff, shape=(dim,) * 2) for dim, diff in differences)
    return reduce(lambda a, f: sp.kronsum(f, a, format='csc'), factors)

#endregion