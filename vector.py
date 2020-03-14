from math import sqrt, acos, pi
from decimal import Decimal, getcontext
import constants

# Decimal used for precision adjustments
getcontext().prec = 30


class Vector(object):

    # CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize to zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            # self.coordinates = tuple(coordinates)
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError("The coordinates must not be empty")

        except TypeError:
            raise TypeError("The coordinates must be an iterable")

    def is_zero(self, tolerance=1e-10):
        """
        Check if vector is 0. Helper function for is_parallel_to()

        :param tolerance: (float) 10 to the minus-10, for precision issues
        :return: (boolean)
        """
        return self.magnitude() < tolerance

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            # multiplies self.coordinates by 1./magnitude
            return self.times_scalar(Decimal('1.0') / magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot_product(self, v):
        try:
            dot_product = [x * y for x, y in zip(self.coordinates, v.coordinates)]
            return sum(dot_product)

        except ValueError:
            raise Exception("Vector lengths must be equal")

    def angle_with(self, v, in_degrees=False):
        try:
            unit_1 = self.normalized()
            unit_2 = v.normalized()
            angle_in_radians = acos(unit_1.dot_product(unit_2))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian

            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with zero vector")
            else:
                raise e

    def is_parallel_to(self, v):
        """
        Check for parallelism between vectors; if two vectors are scalars of one another.
        --> First, if one of the vectors is_zero() == True, then they must be || to one another.
                E.g., for two vectors v1 and v2: if v1.is_zero() == True, then v1 || v2
        --> If v1 and v2 are non-zero, then they must be pointing in the same or opposite direction to be parallel

        :param v: (Vector) second vector for comparison
        :return: (boolean)
        """
        return (
                self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi
                )

    def is_orthogonal_to(self, v, tolerance=1e-10):
        """
        Check if the two vectors have a dot product of 0

        :param v: (Vector) second vector for comparison
        :param tolerance: (float) 10 to the minus-10, for precision issues
        :return: (boolean)
        """
        return abs(self.dot(v)) < tolerance

    def component_parallel_to(self, basis):
        """
        Calculates projected vector ($\vv^||) v in b

        :param basis: (Vector) vector onto which v is projected
        :return: (Vector) projected vector
        """
        try:
            u = basis.normalized()
            weight = self.dot_product(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == constants.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):

        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def projected_vector(self, b):
        """
        Calculates projected vector ($\vv^||) v in b

        :param b: (Vector) vector onto which v is projected
        :return: (Vector) projected vector
        """

        b_normalized = b.normalized()
        return b_normalized.times_scalar(self.dot_product(b_normalized))

    def plus(self, v):
        """
        Add two vectors

        :param v: (Vector) second vector for addition
        :return: (Vector) new vector
        """
        # new_coordinates = []
        # n = len(self.coordinates)
        # for i in range(n):
        #     new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        # return Vector(new_coordinates)
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    #     print(v1.plus(v2)) OR v1.plus(v2).coordinates

    def minus(self, v):
        """
        Difference between two vectors

        :param v: (Vector) second vector for subtaction
        :return: (Vector) the difference between two vectors
        """
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def __str__(self):
        return "Vector: {}".format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


# v1 = Vector([1,2,3])
# v2 = Vector([2.3.4])
# print(v1.add(v2)) OR v1.add(v2).coordinates etc.
