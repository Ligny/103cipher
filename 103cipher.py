'''
 # @ Author: Antoine Deligny
 # @ Create Time: 2021-11-24 14:10:16
 # @ Description:
 '''

import sys
from fractions import Fraction
from typing import List, Union

class MatrixEncryption:
    def __init__(self, message: str, key: str, mode: int):
        self.message = message
        self.key = key
        self.mode = mode
        self.nb = int(len(key) ** 0.5) + 1 if len(key) % 2 != 0 else int(len(key) ** 0.5)
        self.nbr = self.calculate_nbr()
        self.key_matrix = self.calculate_key_matrix()
        self.encrypted_message = self.encrypt_message()

    def calculate_nbr(self) -> int:
        if self.mode == 0:
            return len(self.message) // self.nb + (1 if len(self.message) % self.nb != 0 else 0)
        else:
            return len(self.message.split()) // self.nb + (1 if len(self.message.split()) % self.nb != 0 else 0)

    def calculate_key_matrix(self) -> List[List[Union[int, float]]]:
        key_matrix = []
        k = 0
        for i in range(self.nb):
            key_matrix.append([])
            for j in range(self.nb):
                if k < len(self.key):
                    key_matrix[i].append(ord(self.key[k]))
                    k += 1
                else:
                    key_matrix[i].append(0)
        return key_matrix

    def symmetric_key(self) -> List[List[Union[int, float]]]:
        stock = self.key_matrix[0][1]
        self.key_matrix[0][1] = self.key_matrix[1][0]
        self.key_matrix[1][0] = stock
        stock = self.key_matrix[0][2]
        self.key_matrix[0][2] = self.key_matrix[2][0]
        self.key_matrix[2][0] = stock
        stock = self.key_matrix[1][2]
        self.key_matrix[1][2] = self.key_matrix[2][1]
        self.key_matrix[2][1] = stock
        return self.key_matrix

    def inverse_key(self) -> List[List[float]]:
        det = (
            self.key_matrix[0][0] * (self.key_matrix[1][1] * self.key_matrix[2][2] - self.key_matrix[2][1] * self.key_matrix[1][2])
            - self.key_matrix[0][1] * (self.key_matrix[1][0] * self.key_matrix[2][2] - self.key_matrix[2][0] * self.key_matrix[1][2])
            + self.key_matrix[0][2] * (self.key_matrix[1][0] * self.key_matrix[2][1] - self.key_matrix[2][0] * self.key_matrix[1][1])
        )
        key_int = []
        self.key_matrix = self.symmetric_key()

        for i in range(self.nb):
            key_int.append([])
            for j in range(self.nb):
                key_int[i].append(self.calculate_inverse_element(i, j, det))

        return key_int

    def calculate_inverse_element(self, i: int, j: int, det: float) -> float:
        i_1, i_2 = (1, 2) if i == 0 else (0, 2) if i == 1 else (0, 1)
        j_1, j_2 = (1, 2) if j == 0 else (0, 2) if j == 1 else (0, 1)

        foo = Fraction(1, det)
        result = foo * (self.key_matrix[i_1][j_1] * self.key_matrix[i_2][j_2] - self.key_matrix[i_2][j_1] * self.key_matrix[i_1][j_2])

        fois = -1 if (i, j) in [(0, 1), (1, 0), (2, 1), (1, 2)] else 1

        return float(result * fois) if result != 0 else float(0)

    def encrypt_message(self) -> List[float]:
        result = []
        stock = float(0)

        for i in range(self.nbr):
            for j in range(self.nb):
                for k in range(self.nb):
                    stock += float(self.key_matrix[k][j]) * float(self.message_matrix[i][k])
                result.append(stock)
                stock = float(0)

        return result

    def display_key_matrix(self) -> None:
        for row in self.key_matrix:
            for element in row:
                if self.mode == 0:
                    print(element, end='\t')
                else:
                    print(f'{element:.3f}' if element != 0 else f'{element:.1f}', end='\t')
            print()

    def display_encrypted_message(self) -> None:
        if self.mode == 0:
            print('Encrypted message:')
            for element in self.encrypted_message:
                print(int(element), end=' ')
        else:
            bar = ''.join([chr(int(round(element))) if int(round(element)) != 0 else '' for element in self.encrypted_message])
            print('Encrypted message:\n', bar)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(84)

    mode = int(sys.argv[3])
    if mode != 0 and mode != 1:
        sys.exit(84)

    encryption = MatrixEncryption(sys.argv[1], sys.argv[2], mode)

    print('Key matrix:')
    encryption.display_key_matrix()

    encryption.display_encrypted_message()