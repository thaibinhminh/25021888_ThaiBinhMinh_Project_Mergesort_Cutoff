import java.io.*;
import java.nio.file.*;
import java.util.*;

public class ExperimentRunner {

    // Cố định seed = 42 để đảm bảo tính tái lập khoa học (Reproducibility)
    private static final long SEED = 42L;

    // 3 quy mô kích thước mảng N đủ lớn để loại bỏ nhiễu đồng hồ hệ thống
    private static final int[] SIZES = {100_000, 500_000, 1_000_000};

    // 4 phân phối dữ liệu đặc trưng
    private static final String[] DISTRIBUTIONS = {
        "Random", "Sorted", "Reverse", "NearlySorted"
    };

    // Lưới 14 giá trị CUTOFF (gồm 1 = Baseline, 7 = giáo trình cũ, 10 = giáo trình mới)
    private static final int[] CUTOFFS = {
        1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64
    };

    private static final int WARMUP_RUNS = 5;
    private static final int TRIALS = 15;

    public static void main(String[] args) throws IOException {
        Path datasetDir = Files.exists(Paths.get("../3_Datasets"))
                ? Paths.get("../3_Datasets")
                : Paths.get("3_Datasets");
        Files.createDirectories(datasetDir);

        System.out.println("=================================================================");
        System.out.println("  THI NGHIEM KHAO SAT NGUONG CUTOFF MERGESORT (UET - CHU DE 1.3)");
        System.out.println("=================================================================");
        System.out.println("[1/3] Dang sinh va luu bo du lieu thi nghiem vao: " + datasetDir.toAbsolutePath().normalize());

        Map<String, Integer[]> datasetCache = new LinkedHashMap<>();
        for (int n : SIZES) {
            for (String dist : DISTRIBUTIONS) {
                Integer[] data = generateDataset(n, dist, SEED + n + dist.hashCode());
                Path filePath = datasetDir.resolve(String.format("%s_N%d.txt", dist, n));
                saveDatasetToFile(data, filePath);
                datasetCache.put(dist + "_" + n, data);
            }
        }
        System.out.println("      -> Da sinh thanh cong " + datasetCache.size() + " tep du lieu.");

        System.out.println("[2/3] Dang lam nong JVM (JIT Warm-up)...");
        Integer[] warmupBase = datasetCache.get("Random_100000");
        for (int w = 0; w < WARMUP_RUNS; w++) {
            for (int c : CUTOFFS) {
                Integer[] copy = Arrays.copyOf(warmupBase, warmupBase.length);
                MergeCutoff.sort(copy, c);
            }
        }
        System.out.println("      -> Hoan tat Warm-up.");

        System.out.println("[3/3] Dang do thoi gian thuc nghiem (R = " + TRIALS + " lan/cau hinh)...");
        try (PrintWriter csv = new PrintWriter(new FileWriter("results.csv"))) {
            csv.println("N,Distribution,Cutoff,Trial,TimeMs");

            for (int n : SIZES) {
                for (String dist : DISTRIBUTIONS) {
                    Integer[] original = datasetCache.get(dist + "_" + n);
                    System.out.printf("      -> N = %,10d | Phan phoi = %-12s ... ", n, dist);
                    long t0 = System.currentTimeMillis();

                    for (int c : CUTOFFS) {
                        for (int t = 1; t <= TRIALS; t++) {
                            Integer[] arr = Arrays.copyOf(original, original.length);

                            long start = System.nanoTime();
                            MergeCutoff.sort(arr, c);
                            long end = System.nanoTime();

                            if (!MergeCutoff.isSorted(arr)) {
                                throw new AssertionError("Loi sap xep tai cutoff = " + c);
                            }

                            double timeMs = (end - start) / 1_000_000.0;
                            csv.printf(Locale.US, "%d,%s,%d,%d,%.6f%n", n, dist, c, t, timeMs);
                        }
                    }
                    System.out.printf("Xong (%.2f s)%n", (System.currentTimeMillis() - t0) / 1000.0);
                }
            }
        }
        System.out.println("=================================================================");
        System.out.println("HOAN TAT! Du lieu do tho da luu tai: results.csv");
    }

    private static Integer[] generateDataset(int n, String dist, long seed) {
        Random rng = new Random(seed);
        Integer[] a = new Integer[n];

        switch (dist) {
            case "Random":
                for (int i = 0; i < n; i++) a[i] = rng.nextInt();
                break;
            case "Sorted":
                for (int i = 0; i < n; i++) a[i] = i;
                break;
            case "Reverse":
                for (int i = 0; i < n; i++) a[i] = n - i;
                break;
            case "NearlySorted":
                for (int i = 0; i < n; i++) a[i] = i;
                int swaps = Math.max(1, n / 100);
                for (int s = 0; s < swaps; s++) {
                    int idx1 = rng.nextInt(n);
                    int idx2 = rng.nextInt(n);
                    Integer tmp = a[idx1];
                    a[idx1] = a[idx2];
                    a[idx2] = tmp;
                }
                break;
            default:
                throw new IllegalArgumentException("Phan phoi khong hop le: " + dist);
        }
        return a;
    }

    private static void saveDatasetToFile(Integer[] data, Path filePath) throws IOException {
        try (BufferedWriter bw = Files.newBufferedWriter(filePath)) {
            bw.write(data.length + "\n");
            for (int val : data) {
                bw.write(val + "\n");
            }
        }
    }
}
