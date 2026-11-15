
### 1. Mô hình được chọn
**LinearSVC (C = 1.0, class_weight = None) + TF-IDF n-gram (1, 2)**, ngưỡng quyết định **θ\* = -0.4049** (dò trên OOF của Dev, chọn theo PR-AUC trung bình qua 5-fold CV).

### 2. Kết quả trên Test khóa (N = 4,851; Toxic = 128)

| Chỉ số | Giá trị | CI 95% | Phương pháp CI |
| :--- | :---: | :---: | :---: |
| Accuracy | 0.9878 | [0.9843, 0.9906] | Wilson |
| Toxic Precision | 0.7760 | [0.6953, 0.8402] | Wilson |
| Toxic Recall | 0.7578 | [0.6768, 0.8238] | Wilson |
| Toxic F1 | 0.7668 | [0.7027, 0.8252] | Bootstrap (1000) |
| Macro F1 | 0.8803 | [0.8473, 0.9099] | Bootstrap (1000) |
| PR-AUC | 0.8405 | [0.7813, 0.8952] | Bootstrap (1000) |
| Weighted F1 | 0.9878 | — | — |
| ROC-AUC | 0.9832 | — | — |
| Balanced Accuracy | 0.8759 | — | — |
| MCC | 0.7606 | — | — |

Confusion matrix: TP = 97, FP = 28, FN = 31, TN = 4695.
Vì chỉ có 128 mẫu Toxic trong Test, các khoảng tin cậy khá rộng (CI của Recall rộng 14.7 điểm phần trăm); các chênh lệch nhỏ hơn mức này không nên được diễn giải là khác biệt thật.

### 3. Các phát hiện chính (đều tính từ CV trên Dev)
* **Tiền xử lý:** so với văn bản gốc, tiền xử lý đầy đủ thay đổi Toxic F1 **+1.96 điểm** (có ý nghĩa thống kê (p < 0,05)), Recall **+3.20 điểm** (có ý nghĩa thống kê (p < 0,05)), Precision **+0.10 điểm** (chưa đạt ý nghĩa thống kê (p ≥ 0,05)).
* **BoW so với TF-IDF** (cùng siêu tham số, 15 lượt CV): PR-AUC chênh **+0.0751** (có ý nghĩa thống kê (p < 0,05)); Toxic F1 ở ngưỡng mặc định chênh **-0.0730** (có ý nghĩa thống kê (p < 0,05)).
* **Thuật toán:** cấu hình đứng đầu theo PR-AUC ở baseline là **TF-IDF + LinearSVC** (PR-AUC 0.7967); Naive Bayes tốt nhất là **BoW + MultinomialNB** với PR-AUC 0.3362.
* **Dò ngưỡng:** trên OOF, dịch ngưỡng từ 0 sang -0.4049 làm Recall 0.4882 → 0.7523, Precision 0.9337 → 0.7543, F1 0.6412 → 0.7533. Trên Test, F1 là 0.6492 ở ngưỡng mặc định và 0.7668 ở θ\*.
* **Độ ổn định:** Toxic F1 qua 15 lượt CV là 0.6402 ± 0.0376 (ngưỡng mặc định).
* **Độ nhạy với near-duplicate:** loại 339 mẫu near-duplicate làm F1 thay đổi -0.0057.
* **Suy luận:** 0.112 ms/bình luận khi xử lý theo lô, 0.654 ms/bình luận khi xử lý từng cái (AMD64 Family 25 Model 80 Stepping 0, AuthenticAMD, 12 luồng).

### 4. Hạn chế
1. **Bộ nhãn đã được con người kiểm định độc lập**, theo xác nhận của người thực hiện nghiên cứu. Báo cáo cần mô tả quy trình kiểm định đã thực hiện; chỉ trình bày tỷ lệ sửa nhãn hoặc độ đồng thuận khi có thống kê thực tế. Tệp `label_audit_sample.csv` phục vụ rà soát bổ sung, không phải điều kiện kiểm định còn thiếu.
2. **Số mẫu Toxic trong Test ít**, nên mọi chỉ số của lớp Toxic có sai số lấy mẫu đáng kể (xem CI).
3. **Một chủ đề, một nền tảng, một khoảng thời gian** (bình luận về một bộ phim trên Facebook). Chưa có bằng chứng về khả năng tổng quát hóa sang chủ đề khác.
4. **Mô hình n-gram không hiểu ngữ cảnh**: mỉa mai, ẩn ý và chuỗi trả lời (thread) không được xử lý.
5. **Từ điển teencode là lựa chọn thủ công**: các ánh xạ như `cc`, `vc` có thể sinh báo động giả khi người dùng dùng với nghĩa khác (ví dụ `cc` = "các cậu").
6. **Chưa có nhóm theo bài đăng/người dùng** trong dữ liệu nên việc chia ngẫu nhiên không loại trừ được phụ thuộc theo bài đăng hoặc theo tác giả.

### 5. Hướng phát triển
Kiểm định nhãn bởi người và đo độ đồng thuận (Cohen's κ); gắn nhóm theo bài đăng để chia `GroupKFold`; thử mô hình tiền huấn luyện tiếng Việt (PhoBERT, ViSoBERT) và so sánh với baseline này trên **cùng** Test khóa.
