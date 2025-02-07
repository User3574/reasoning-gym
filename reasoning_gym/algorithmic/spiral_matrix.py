"""Print elements of a matrix in spiral order.

A popular Leetcode problem:
https://leetcode.com/problems/spiral-matrix/description/
"""

from dataclasses import dataclass
from random import Random
from typing import Optional

from ..factory import ProceduralDataset, register_dataset

QUESTION_TEMPLATE = """Given a matrix, your job is to generate a list of elements in spiral order.

Example:

Input: 
1 2 3 4
5 6 7 8
9 10 11 12

Output: 1 2 3 4 8 12 11 10 9 5 6 7

For the matrix below, what is the list of elements in spiral order?
{matrix}
"""


@dataclass
class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    max_rows: int = 10 # Maximum number of rows in the matrix
    max_cols: int = 10 # Maximum number of columns in the matrix

    size: int = 500  # Virtual dataset size
    seed: Optional[int] = None

    def validate(self):
        """Validate configuration parameters"""
        assert 1 <= self.max_rows, "max_rows must be at least 1"
        assert 1 <= self.max_cols, "max_cols must be at least 1"


class SpiralMatrixDataset(ProceduralDataset):
    """Generates Spiral Matrix exercises with configurable difficulty"""

    def __init__(self, config: SpiralMatrixConfig):
        super().__init__(config=config, seed=config.seed, size=config.size)

    def _get_matrix(self, rng: Random) -> list[list[int]]:
        """Generate a random matrix"""
        rows, cols = rng.randint(1, self.config.max_rows), rng.randint(1, self.config.max_cols)
        numbers = list(range(rows * cols))
        rng.shuffle(numbers)
        matrix = [numbers[i * cols : (i + 1) * cols] for i in range(rows)]
        return matrix

    def _get_spiral(self, matrix: list[list[int]]) -> list[int]:
        """Return the elements of the matrix in spiral order"""
        t, b = 0, len(matrix)
        l, r = 0, len(matrix[0])

        out = []

        while True:
            for i in range(l, r):
                out.append(matrix[t][i])
            t += 1
            if t == b: break

            for i in range(t, b):
                out.append(matrix[i][r-1])
            r -= 1
            if l == r: break

            for i in range(r-1, l-1, -1):
                out.append(matrix[b-1][i])
            b -= 1
            if t == b: break

            for i in range(b-1, t-1, -1):
                out.append(matrix[i][l])
            l += 1
            if l == r: break

        return out
    
    def _matrix_to_str(self, matrix: list[list[int]]) -> str:
        """Get a string representation of the matrix"""
        return "\n".join(" ".join(str(x) for x in row) for row in matrix)
    
    def _list_to_str(self, array: list[int]) -> str:
        """Get a string representation of the array"""
        return " ".join(str(x) for x in array)

    def __getitem__(self, idx: int) -> dict:
        """Generate a single Spiral Matrix question"""
        rng = Random(self.seed + idx)
        
        matrix = self._get_matrix(rng)
        matrix_str = self._matrix_to_str(matrix)
        answer = self._get_spiral(matrix)
        answer_str = self._list_to_str(answer)

        return {
            "question": QUESTION_TEMPLATE.format(matrix=matrix_str),
            "answer": answer_str,
            "metadata": {"matrix": matrix, "solution": answer},
        }


register_dataset("spiral_matrix", SpiralMatrixDataset, SpiralMatrixConfig)
