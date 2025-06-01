#keerthana srinivasan
#5/28/2025

import streamlit as st #streamlit for UI
from streamlit_option_menu import option_menu #menu on the side
import random #generate random numbers
import time #track runtime of sorting algorithms
import pandas as pd #present tabular data
from io import StringIO #handle in-memory CSV data

#bubble sort with intermediate steps using yield
def bubble_sort_yield(arr):
    N = len(arr) #number of elements in array
    #for each element in the array, 
    for i in range(N):
        for j in range(0, N - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  #swap if elements are out of order (from least to greatest)
                yield arr #present the final array!

#insertion sort with yield
def insertion_sort_yield(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        #shift elements until correct spot for key is found
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

#selection sort with yield
def selection_sort_yield(arr):
    for i in range(len(arr)):
        min_idx = i
        #find index of minimum element
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

#heap sort with yield
def heap_sort_yield(arr):
    #helper function to maintain heap property
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1 #left child
        r = 2 * i + 2 #right child
        #check if left or right child is greater
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        #if needed, swap and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr
            yield from heapify(arr, n, largest)

    n = len(arr)
    #build max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    #extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)

#merge sort with yield
def merge_sort_yield(arr):
    #recursive merge sort
    def merge_sort_gen(arr, l, r):
        if l < r:
            m = (l + r) // 2
            yield from merge_sort_gen(arr, l, m)
            yield from merge_sort_gen(arr, m + 1, r)
            yield from merge(arr, l, m, r)
    #helper to merge two sorted halves
    def merge(arr, l, m, r):
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l
        #merge the two halves
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            yield arr
        #add any remaining elements
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

#sidebar navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Sorting Algorithms", "Data Visualization"],
        icons=["house", "sort-up", "bar-chart"],
        default_index=0,
    )

#home page
def home():
    st.title("Sorting Algorithms Visualizer")
    st.write("Visualize classic sorting algorithms in real-time.")
    st.write("Choose an algorithm and array size to begin.")

#sorting algorithm visualizer
def sorting_algorithms():
    st.title("Sorting Algorithms")
    st.write("Choose an algorithm and visualize how it sorts an array.")
    
    #user selects algorithm, array size, and speed
    algo = st.selectbox("Select Sorting Algorithm", [
        "Bubble Sort", "Insertion Sort", "Selection Sort", "Heap Sort", "Merge Sort"
    ])

    array_size = st.slider("Array Size", min_value=10, max_value=200, value=50)
    speed = st.slider("Animation Delay (seconds)", min_value=0.01, max_value=0.5, value=0.05)

    if st.button("Run Sort"):
        arr = [random.randint(1, 100) for _ in range(array_size)]
        chart_placeholder = st.empty()
        #map selected algorithm to its function
        algo_map = {
            "Bubble Sort": bubble_sort_yield,
            "Insertion Sort": insertion_sort_yield,
            "Selection Sort": selection_sort_yield,
            "Heap Sort": heap_sort_yield,
            "Merge Sort": merge_sort_yield
        }

        sorter = algo_map[algo]
        arr_copy = arr.copy()

        #animate each sorting step
        for step in sorter(arr_copy):
            chart_placeholder.bar_chart(step)
            time.sleep(speed)

        st.success("Sorting complete!")

#sorting algorithm performance comparison
def data_analysis():
    st.title("Sorting Algorithm Time Comparison")
    array_size = st.slider("Array Size", min_value=10, max_value=10000, value=100)

    run = st.button("Run Data Analysis")

    if run:
        result = []
        #for large arrays, skip slow algorithms
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

        #measure time taken by each algorithm
        for name, sorter in algorithms.items():
            arr = [random.randint(1, 100) for _ in range(array_size)]
            arr_copy = arr.copy()
            start_time = time.time()
            for _ in sorter(arr_copy):
                pass
            elapsed_time = time.time() - start_time
            result.append({"Algorithm": name, "Time (s)": round(elapsed_time, 6)})
        #show results in table and allow CSV download
        df_result = pd.DataFrame(result).sort_values(by="Time (s)")
        st.dataframe(df_result, use_container_width=True)

        csv = df_result.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='sorting_analysis.csv',
            mime='text/csv',
        )

#route based on selected menu option
if selected == "Home":
    home()
elif selected == "Sorting Algorithms":
    sorting_algorithms()
elif selected == "Data Visualization":
    data_analysis()
