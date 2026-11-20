public class MergeCutoff {

    // Không khởi tạo đối tượng tiện ích
    private MergeCutoff() {}

    /**
     * Sắp xếp chèn (Insertion Sort) trên đoạn a[lo..hi].
     * Chuẩn hóa theo quy ước giáo trình Algorithms (Sedgewick & Wayne).
     */
    private static void insertionSort(Comparable[] a, int lo, int hi) {
        for (int i = lo + 1; i <= hi; i++) {
            Comparable v = a[i];
            int j = i;
            while (j > lo && less(v, a[j - 1])) {
                a[j] = a[j - 1];
                j--;
            }
            a[j] = v;
        }
    }

    /**
     * Trộn hai nửa đã sắp xếp a[lo..mid] và a[mid+1..hi].
     * Tối ưu mảng phụ nửa kích thước (a.length / 2 + 1) theo bài giảng UET:
     * - Chỉ sao chép nửa trái a[lo..mid] sang aux[0..mid-lo].
     * - Nửa phải a[mid+1..hi] giữ nguyên tại chỗ trên mảng a[].
     * - Bất biến vòng lặp: con trỏ ghi k luôn thỏa mãn k <= j, do đó các phần tử
     *   chưa xét ở nửa phải không bao giờ bị ghi đè trước khi được đọc.
     */
    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {
        for (int i = 0; i <= mid - lo; i++) {
            aux[i] = a[lo + i];
        }

        int i = 0;
        int j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if      (i > mid - lo)       a[k] = a[j++];
            else if (j > hi)             a[k] = aux[i++];
            else if (less(a[j], aux[i])) a[k] = a[j++];
            else                         a[k] = aux[i++];
        }
    }

    /**
     * Đệ quy Top-down Mergesort kết hợp ngưỡng CUTOFF chuẩn giáo trình:
     * 1. Mảng con có độ dài <= cutoff (hi <= lo + cutoff - 1) chuyển sang Insertion Sort.
     * 2. Bỏ qua bước merge() nếu hai nửa đã có thứ tự tự nhiên (a[mid] <= a[mid + 1]),
     *    giúp giảm độ phức tạp xuống O(N) trên dữ liệu Sorted và NearlySorted.
     */
    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi, int cutoff) {
        if (hi <= lo) return;
        if (hi <= lo + cutoff - 1) {
            insertionSort(a, lo, hi);
            return;
        }
        int mid = lo + (hi - lo) / 2;
        sort(a, aux, lo, mid, cutoff);
        sort(a, aux, mid + 1, hi, cutoff);

        // Tối ưu Skip-Merge (Sedgewick): nếu phần tử lớn nhất nửa trái <= phần tử nhỏ nhất nửa phải
        // thì toàn bộ đoạn a[lo..hi] đã có thứ tự, không cần sao chép và trộn.
        if (!less(a[mid + 1], a[mid])) return;

        merge(a, aux, lo, mid, hi);
    }

    /**
     * Giao diện công khai sắp xếp mảng a[] với ngưỡng cutoff cho trước.
     */
    public static void sort(Comparable[] a, int cutoff) {
        Comparable[] aux = new Comparable[a.length / 2 + 1];
        sort(a, aux, 0, a.length - 1, cutoff);
    }

    @SuppressWarnings("unchecked")
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    /**
     * Kiểm tra hậu điều kiện mảng đã được sắp xếp tăng dần.
     */
    public static boolean isSorted(Comparable[] a) {
        for (int i = 1; i < a.length; i++) {
            if (less(a[i], a[i - 1])) return false;
        }
        return true;
    }
}