from dataclasses import dataclass
from aocd import get_data


@dataclass
class Tree:
    Height: int
    Row: int
    Column: int


@dataclass
class ScenicScore:
    Left: int
    Right: int
    Top: int
    Bottom: int
    Data: Tree

    def compute(self):
        return self.Left * self.Right * self.Top * self.Bottom


def filter_view(tree_height: int, comparison_trees: list[int]) -> int:
    count = 0
    for comparison_tree in comparison_trees:
        if comparison_tree < tree_height:
            count += 1
        if comparison_tree >= tree_height:
            count += 1
            break
    return count


def part2(input_matrix: list, start_row_index: int, start_column_index: int) -> list[ScenicScore]:
    scores = []
    for current_row_index in range(start_row_index, rows - 1):
        for current_column_index in range(start_column_index, columns - 1):
            current_tree_height = int(input_matrix[current_row_index][current_column_index])
            current_tree = Tree(current_tree_height, current_row_index, current_column_index)
            new_score = ScenicScore(0, 0, 0, 0, current_tree)

            current_row_look_left = list(map(int, input_matrix[current_row_index][:current_column_index]))
            current_row_look_left.reverse()
            new_score.Left = filter_view(current_tree_height, current_row_look_left)
            new_score.Right = filter_view(current_tree_height,
                                          list(map(int, input_matrix[current_row_index][current_column_index + 1:])))

            current_column_look_up = [int(input_matrix[lookup_row_index_up][current_column_index]) for
                                      lookup_row_index_up in range(0, current_row_index)]
            current_column_look_up.reverse()
            new_score.Top = filter_view(current_tree_height, current_column_look_up)

            current_column_look_down = [int(input_matrix[lookup_row_index_down][current_column_index]) for
                                        lookup_row_index_down in range(current_row_index + 1, len(input_matrix))]
            new_score.Bottom = filter_view(current_tree_height, current_column_look_down)
            scores.append(new_score)
    return scores


def is_tree_visible(tree_height: int, comparison_trees: list[int]) -> bool:
    return all(z < tree_height for z in comparison_trees)


def part1(input_matrix: list, start_row_index: int, start_column_index: int) -> int:
    visible_trees = 0
    for current_row_index in range(start_row_index, rows - 1):
        for current_column_index in range(start_column_index, columns - 1):
            current_tree_height = int(input_matrix[current_row_index][current_column_index])
            current_row_look_left = list(map(int, input_matrix[current_row_index][:current_column_index]))
            if is_tree_visible(current_tree_height, current_row_look_left):
                visible_trees += 1
                continue
            current_row_look_right = list(map(int, input_matrix[current_row_index][current_column_index + 1:]))
            if is_tree_visible(current_tree_height, current_row_look_right):
                visible_trees += 1
                continue
            current_column_look_up = [int(input_matrix[lookup_row_index_up][current_column_index]) for
                                      lookup_row_index_up in range(0, current_row_index)]
            if is_tree_visible(current_tree_height, current_column_look_up):
                visible_trees += 1
                continue
            current_column_look_down = [int(input_matrix[lookup_row_index_down][current_column_index]) for
                                        lookup_row_index_down in range(current_row_index + 1, len(input_matrix))]
            if is_tree_visible(current_tree_height, current_column_look_down):
                visible_trees += 1
                continue

    return visible_trees


if __name__ == '__main__':
    data = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390'
    ]
    data = get_data(day=8, year=2022).splitlines()
    rows = len(data[0])
    columns = len(data)

    exterior_trees = rows + (rows - 1) + (columns - 1) + (columns - 2)
    matrix = [list(row) for row in data]
    visible_trees = part1(matrix, 1, 1)
    print(f'Part 1: {visible_trees + exterior_trees}')

    max_tree_score = max([x.compute() for x in part2(matrix, 1, 1)])
    print(f'Part 2: {max_tree_score}')
