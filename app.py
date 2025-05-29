import streamlit as st
from streamlit_option_menu import option_menu
import random
import time
import pandas as pd
from io import StringIO

def bubble_sort_yield(arr):
    N = len(arr)
    for i in range(N):
        for j in range(0, N - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr

def insertion_sort_yield(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

def selection_sort_yield(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def heap_sort_yield(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr
            yield from heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)

def merge_sort_yield(arr):
    def merge_sort_gen(arr, l, r):
        if l < r:
            m = (l + r) // 2
            yield from merge_sort_gen(arr, l, m)
            yield from merge_sort_gen(arr, m + 1, r)
            yield from merge(arr, l, m, r)

    def merge(arr, l, m, r):
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            yield arr
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            yield arr
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            yield arr

    yield from merge_sort_gen(arr, 0, len(arr) - 1)


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Sorting Algorithms", "Data Visualization"],
        icons=["house", "sort-up", "bar-chart"],
        default_index=0,
    )


def home():
    st.title("Sorting Algorithms Visualizer")
    st.write("Visualize classic sorting algorithms in real-time.")
    st.write("Choose an algorithm and array size to begin.")


def sorting_algorithms():
    st.title("Sorting Algorithms")
    st.write("Choose an algorithm and visualize how it sorts an array.")

    algo = st.selectbox("Select Sorting Algorithm", [
        "Bubble Sort", "Insertion Sort", "Selection Sort", "Heap Sort", "Merge Sort"
    ])

    array_size = st.slider("Array Size", min_value=10, max_value=200, value=50)
    speed = st.slider("Animation Delay (seconds)", min_value=0.01, max_value=0.5, value=0.05)

    if st.button("Run Sort"):
        arr = [random.randint(1, 100) for _ in range(array_size)]
        chart_placeholder = st.empty()

        algo_map = {
            "Bubble Sort": bubble_sort_yield,
            "Insertion Sort": insertion_sort_yield,
            "Selection Sort": selection_sort_yield,
            "Heap Sort": heap_sort_yield,
            "Merge Sort": merge_sort_yield
        }

        sorter = algo_map[algo]
        arr_copy = arr.copy()

        for step in sorter(arr_copy):
            chart_placeholder.bar_chart(step)
            time.sleep(speed)

        st.success("Sorting complete!")


def data_analysis():
    st.title("Sorting Algorithm Time Comparison")
    array_size = st.slider("Array Size", min_value=10, max_value=10000, value=100)

    run = st.button("Run Data Analysis")

    if run:
        result = []
        if array_size > 1000:
            algorithms = {
                "Selection Sort": selection_sort_yield,
                "Heap Sort": heap_sort_yield,
                "Merge Sort": merge_sort_yield
            }
        else:
            algorithms = {
                "Bubble Sort": bubble_sort_yield,
                "Insertion Sort": insertion_sort_yield,
                "Selection Sort": selection_sort_yield,
                "Heap Sort": heap_sort_yield,
                "Merge Sort": merge_sort_yield
            }

        for name, sorter in algorithms.items():
            arr = [random.randint(1, 100) for _ in range(array_size)]
            arr_copy = arr.copy()
            start_time = time.time()
            for _ in sorter(arr_copy):
                pass
            elapsed_time = time.time() - start_time
            result.append({"Algorithm": name, "Time (s)": round(elapsed_time, 6)})

        df_result = pd.DataFrame(result).sort_values(by="Time (s)")
        st.dataframe(df_result, use_container_width=True)

        csv = df_result.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='sorting_analysis.csv',
            mime='text/csv',
        )

if selected == "Home":
    home()
elif selected == "Sorting Algorithms":
    sorting_algorithms()
elif selected == "Data Visualization":
    data_analysis()
