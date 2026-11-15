# Đánh giá kết quả thực nghiệm phân loại bình luận Toxic về phim “Mưa đỏ”

Ngày đánh giá: 16/11/2026 (Asia/Bangkok).

## 1. Mục tiêu và phạm vi

Thực nghiệm nhằm so sánh các thuật toán học máy truyền thống trong phân loại bình luận tiếng Việt thành hai lớp: Toxic và Non-toxic. Bản đánh giá sử dụng kết quả chạy lại toàn bộ notebook `benchmark_toxic_v2.ipynb` trên dữ liệu `mua_do_comments_labeled_final.csv` được cung cấp.

Notebook đã chạy hoàn tất 19 ô mã từ một phiên làm việc mới, không có ô mã nào kết thúc bằng lỗi. Các bảng kết quả, biểu đồ, dự đoán và mô hình đã được xuất ra tệp. Theo xác nhận của người thực hiện nghiên cứu, bộ nhãn ban đầu do mô hình ngôn ngữ lớn (LLM) gán đã được con người kiểm định độc lập. Các chỉ số được đánh giá trên bộ nhãn cuối cùng này.

## 2. Dữ liệu và thiết kế thực nghiệm

Dữ liệu ban đầu gồm 24.491 bình luận, trong đó có 641 bình luận Toxic, chiếm khoảng 2,62%. Đây là bài toán mất cân bằng lớp rõ rệt, nên Accuracy không phù hợp làm tiêu chí đánh giá chính.

Quá trình làm sạch loại bỏ 21 bình luận rỗng sau tiền xử lý, 2 dòng thuộc một nhóm nội dung trùng nhưng nhãn mâu thuẫn và 214 bản sao thừa của các nhóm trùng có nhãn nhất quán. Dữ liệu thực nghiệm còn 24.254 bình luận, gồm 638 Toxic và 23.616 Non-toxic.

| Tập dữ liệu | Tổng số bình luận | Toxic | Non-toxic |
|---|---:|---:|---:|
| Phát triển (Dev) | 19.403 | 510 | 18.893 |
| Kiểm tra (Test) | 4.851 | 128 | 4.723 |

Dữ liệu được chia có phân tầng theo nhãn, với tỷ lệ Dev/Test xấp xỉ 80/20 và hạt giống ngẫu nhiên bằng 42. Không có nội dung trùng chính xác sau chuẩn hóa giữa hai tập. Bộ vector hóa nằm trong pipeline và chỉ học từ phần huấn luyện của từng lượt đánh giá chéo.

Thực nghiệm bao gồm 10 cấu hình cơ sở từ 5 thuật toán kết hợp với BoW hoặc TF-IDF; phân tích ảnh hưởng của tiền xử lý trên 15 lượt đánh giá chéo; tìm kiếm 20 cấu hình LinearSVC; so sánh BoW với TF-IDF; và lựa chọn ngưỡng từ điểm ngoài mẫu (OOF) trên Dev. Test không được dùng để lựa chọn siêu tham số hoặc ngưỡng.

## 3. Kết quả lựa chọn mô hình

Trong nhóm cấu hình cơ sở, TF-IDF kết hợp LinearSVC đạt Average Precision trung bình cao nhất trên đánh giá chéo, bằng 0,7967. Sau tối ưu siêu tham số, cấu hình được chọn đạt Average Precision trung bình 0,8104 trên 5 fold của Dev.

Cấu hình cuối cùng gồm:

- Biểu diễn văn bản: TF-IDF với unigram và bigram, tức n-gram từ 1 đến 2.
- Thuật toán: LinearSVC, tham số `C = 1,0`, `class_weight = None`.
- Ngưỡng phân loại: −0,4048915; dự đoán Toxic khi điểm quyết định lớn hơn hoặc bằng ngưỡng này.

Ngưỡng được chọn để tối đa hóa F1 của lớp Toxic trên điểm OOF của Dev. Do cùng các điểm OOF được dùng để chọn và tính hiệu quả của ngưỡng, kết quả OOF sau tối ưu có thể lạc quan. Kết quả Test là căn cứ chính để đánh giá mô hình cuối cùng.

## 4. Kết quả trên tập kiểm tra

| Chỉ số | Giá trị | Khoảng tin cậy 95% |
|---|---:|---:|
| Precision của lớp Toxic | 0,7760 | [0,6953; 0,8402] |
| Recall của lớp Toxic | 0,7578 | [0,6768; 0,8238] |
| F1 của lớp Toxic | 0,7668 | [0,7027; 0,8252] |
| Macro F1 | 0,8803 | [0,8473; 0,9099] |
| Average Precision (AP) | 0,8405 | [0,7813; 0,8952] |
| Accuracy | 0,9878 | [0,9843; 0,9906] |

Khoảng tin cậy của Precision, Recall và Accuracy được tính theo phương pháp Wilson. Khoảng tin cậy của F1, Macro F1 và AP được ước lượng bằng 1.000 lần lấy mẫu bootstrap trên Test. Các khoảng này có điều kiện trên mô hình đã huấn luyện, chưa bao gồm toàn bộ biến thiên do lựa chọn mô hình hoặc thay đổi tập huấn luyện.

Ma trận nhầm lẫn:

| Nhãn thực tế | Dự đoán Non-toxic | Dự đoán Toxic |
|---|---:|---:|
| Non-toxic | 4.695 | 28 |
| Toxic | 31 | 97 |

Mô hình phát hiện đúng 97/128 bình luận Toxic, tương ứng Recall 75,78%, nhưng còn bỏ sót 31 bình luận, tương ứng 24,22%. Trong 125 bình luận được dự đoán là Toxic, có 28 báo động giả theo nhãn hiện có, chiếm 22,40%.

Accuracy đạt 98,78%, nhưng luôn dự đoán Non-toxic cũng đạt khoảng 97,36% trên Test. Vì vậy, báo cáo nên ưu tiên F1, Precision, Recall của lớp Toxic và AP; chỉ dùng Accuracy làm thông tin bổ sung.

## 5. Ảnh hưởng của tiền xử lý và ngưỡng dự đoán

Tiền xử lý đầy đủ giúp F1 của lớp Toxic tăng trung bình khoảng 1,96 điểm phần trăm so với văn bản gốc trên 15 lượt đánh giá chéo. Kiểm định cặp có hiệu chỉnh đang dùng cho kết quả p = 0,01965. Các p-value chưa được hiệu chỉnh cho nhiều phép so sánh, nên cần trình bày phát hiện này theo hướng thăm dò, tránh khẳng định quá mức về ý nghĩa thống kê.

Việc điều chỉnh ngưỡng cho thấy sự đánh đổi rõ ràng trên Test:

| Chỉ số lớp Toxic | Ngưỡng mặc định 0 | Ngưỡng đã chọn −0,4049 |
|---|---:|---:|
| Precision | 0,9841 | 0,7760 |
| Recall | 0,4844 | 0,7578 |
| F1 | 0,6492 | 0,7668 |

Ngưỡng được chọn giúp phát hiện thêm nhiều bình luận Toxic và tăng F1, đồng thời làm tăng báo động giả. Kết quả này thể hiện sự cân bằng Precision/Recall phù hợp hơn với mục tiêu tối đa hóa F1, không phải cải thiện đồng thời mọi chỉ số.

## 6. Độ nhạy với bình luận gần trùng

Kiểm tra độ tương đồng cosine trên biểu diễn TF-IDF từ, với ngưỡng 0,90, phát hiện 339 bình luận Test gần trùng Dev, trong đó có 3 bình luận Toxic.

Sau khi loại nhóm này, tập đánh giá còn 4.512 bình luận, gồm 125 Toxic. Precision đạt 0,7705, Recall đạt 0,7520 và F1 đạt 0,7611. F1 giảm khoảng 0,57 điểm phần trăm so với toàn bộ Test.

Trong phạm vi phép kiểm tra đang dùng, kết quả ít thay đổi khi loại các mẫu gần trùng. Tuy nhiên, phép kiểm tra chưa loại trừ mọi dạng tương đồng ngữ nghĩa hoặc phụ thuộc theo bài đăng, người dùng và chuỗi hội thoại.

## 7. Hạn chế và nội dung cần hoàn thiện

### 7.1. Tình trạng kiểm định nhãn

Bộ dữ liệu gán nhãn đã được con người kiểm định độc lập theo xác nhận của người thực hiện nghiên cứu. Vì vậy, nhận định trước đây rằng bộ nhãn chưa được kiểm định không còn phù hợp và không được sử dụng làm lý do trì hoãn báo cáo.

Trong phần mô tả dữ liệu của báo cáo, nên ghi rõ tiêu chí phân loại Toxic, phạm vi kiểm định, số người tham gia và cách xử lý bất đồng theo quy trình đã thực hiện. Chỉ đưa số liệu về tỷ lệ sửa nhãn hoặc độ đồng thuận khi có thống kê thực tế; bản đánh giá này chưa có các thông tin đó và không suy đoán thêm.

Tệp `label_audit_sample.csv` gồm 59 ca dự đoán sai và 50 ca dự đoán đúng do notebook xuất để hỗ trợ phân tích bổ sung. Đây không phải bằng chứng rằng bộ dữ liệu chưa được kiểm định, cũng không phải mẫu đại diện để ước lượng tỷ lệ sai nhãn toàn bộ dữ liệu.

### 7.2. Diễn giải thống kê và tên chỉ số

Các cột `PR-AUC` trong notebook thực tế được tính bằng `average_precision_score`. Báo cáo nên gọi rõ là Average Precision (AP), tránh đồng nhất với diện tích dưới đường Precision–Recall tính bằng quy tắc hình thang.

Nhận định rằng `Gap_in_Std < 1` chứng minh hai cấu hình không khác biệt về thống kê cần được sửa: đây chỉ là đại lượng mô tả khoảng cách, không phải phép kiểm định. Tương tự, độ rộng khoảng tin cậy của Recall không phải ngưỡng xác định chênh lệch giữa hai mô hình có ý nghĩa thống kê hay không.

CV dùng để lựa chọn cấu hình không tạo thành đánh giá chéo lồng nhau (nested CV). Phép so sánh BoW/TF-IDF dùng siêu tham số đã chọn cho TF-IDF, nên chưa đủ để kết luận TF-IDF luôn tốt hơn BoW khi cả hai được tối ưu riêng.

### 7.3. Cảnh báo huấn luyện và khả năng tái lập

Lần chạy có cảnh báo chưa hội tụ (`ConvergenceWarning`) trong benchmark và lỗi dọn tài nguyên `joblib.resource_tracker` khi đóng kernel. Các ô mã vẫn hoàn thành. Mô hình cuối đã được nạp trong tiến trình mới và tái tạo đúng toàn bộ điểm quyết định cùng nhãn dự đoán trên Test.

Trước khi tuyên bố mọi cấu hình đã hội tụ, cần ghi nhận cảnh báo theo thuật toán và fold, sau đó kiểm tra lại cấu hình gây cảnh báo. Notebook hiện bỏ qua cảnh báo ở tiến trình chính, nên cần điều chỉnh cách ghi nhận khi hoàn thiện bản cuối.

Tệp `requirements_runtime.txt` đã bổ sung các thư viện chính phục vụ chạy notebook, gồm Matplotlib và các thành phần Jupyter. Matplotlib được cài tại `.runtime`; `run_benchmark.py` thêm đường dẫn này vào bản notebook chạy lại. Mã SHA-256 của dữ liệu và notebook gốc được lưu trong `input_sha256.json` để đối chiếu đầu vào.

### 7.4. Phạm vi khái quát hóa

Dữ liệu chỉ phản ánh bình luận về một bộ phim trên Facebook. Kết quả hiện tại chưa chứng minh khả năng áp dụng sang chủ đề, nền tảng hoặc thời gian khác. Dữ liệu chưa có thông tin nhóm bài đăng/người dùng để đánh giá độc lập theo các nhóm này.

Test đã được xem để lập bản đánh giá này. Nếu tiếp tục dùng kết quả Test để lựa chọn mô hình, tiền xử lý hoặc ngưỡng, cần có tập kiểm tra độc lập mới cho kết luận cuối cùng.

## 8. Mức độ sẵn sàng để báo cáo

**Notebook đã có đủ kết quả thực nghiệm để đưa vào báo cáo, với bộ nhãn đã được con người kiểm định độc lập. Trước khi chốt bản cuối, cần hoàn thiện diễn giải thống kê và làm rõ cảnh báo hội tụ.**

Các nội dung đã có gồm quy trình chạy đầy đủ, so sánh mô hình, tối ưu siêu tham số, lựa chọn ngưỡng trên Dev, đánh giá Test kèm khoảng tin cậy, phân tích lỗi và kiểm tra độ nhạy với bình luận gần trùng. Bản notebook đã chạy có 9 biểu đồ và không có ô mã lỗi.

Để chốt báo cáo, cần mô tả quy trình kiểm định nhãn đã thực hiện, sửa tên chỉ số và diễn giải thống kê, đồng thời làm rõ cảnh báo hội tụ. Không cần yêu cầu kiểm định lại chỉ vì nhãn ban đầu do LLM gán. Khoảng tin cậy 95% của Toxic F1 còn khá rộng, từ 0,7027 đến 0,8252, nên tránh diễn giải những chênh lệch nhỏ như bằng chứng chắc chắn về ưu thế của mô hình.

## 9. Các tệp phục vụ báo cáo

- `benchmark_toxic_v2_executed.ipynb`: notebook đã chạy, gồm bảng kết quả, kết luận và 9 biểu đồ được nhúng từ ảnh sinh trong lần chạy.
- `BENCHMARK_TOXIC/results/test_metrics.csv`: chỉ số Test và khoảng tin cậy.
- `BENCHMARK_TOXIC/results/experiment_summary.json`: cấu hình, kết quả, độ trễ và phiên bản thư viện.
- `BENCHMARK_TOXIC/results/test_predictions.csv`: dự đoán từng mẫu Test.
- `BENCHMARK_TOXIC/results/error_analysis.csv`: ca dự đoán sai và đặc trưng đóng góp.
- `BENCHMARK_TOXIC/results/label_audit_sample.csv`: mẫu hỗ trợ kiểm định nhãn.
- `BENCHMARK_TOXIC/figures`: 9 biểu đồ PNG.
- `BENCHMARK_TOXIC/models/best_model.joblib` và `BENCHMARK_TOXIC/toxic_preprocess.py`: mô hình và mô-đun tiền xử lý cần giữ để nạp lại.
- `BENCHMARK_TOXIC/results/requirements_runtime.txt` và `BENCHMARK_TOXIC/results/input_sha256.json`: thông tin hỗ trợ tái lập và đối chiếu đầu vào.

Notebook gốc được giữ nguyên. Bản đánh giá này làm rõ các điều kiện và giới hạn khi sử dụng kết quả thực nghiệm trong báo cáo.
