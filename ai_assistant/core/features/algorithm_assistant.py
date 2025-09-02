class AlgorithmSolver:
    def solve_sorting(self, arr):
        """Minh họa giải thuật sắp xếp nổi bọt (Bubble Sort)"""
        steps = []
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append(arr.copy())
        return steps

    def explain_sorting(self):
        return (
            "👨‍💻 Giải thuật sắp xếp nổi bọt (Bubble Sort):\n"
            "- So sánh từng cặp phần tử liên tiếp.\n"
            "- Hoán đổi nếu sai thứ tự.\n"
            "- Lặp lại cho tới khi mảng được sắp xếp.\n"
            "- Độ phức tạp: O(n^2)."
        )
