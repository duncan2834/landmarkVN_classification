import torch
from torchvision import models, transforms, datasets
import torch.nn as nn
from PIL import Image
import gradio as gr
import os


landmark_info = {
    "Vịnh_Hạ_Long": "Vịnh Hạ Long là một Vịnh thuộc tỉnh Quảng Ninh, Việt Nam. Vịnh từng được UNESCO nhiều lần công nhận là Di sản thiên nhiên của Thế Giới. Vịnh nổi tiếng với gần 2000 hòn đảo lớn nhỏ, đặc biệt là đảo đá vôi, trải dài trên 1.553 km2. Trong đó, vùng lõi Vịnh rộng 335 km2, tập trung dày đặc 775 hòn đảo.",
    "Núi_Yên_Tử": "Núi Yên Tử nằm ở khu vực ranh giới giữa hai tỉnh Quảng Ninh và Bắc Giang, cách trung tâm Hà Nội khoảng 130km. Nơi đây nổi tiếng với vẻ đẹp thiên nhiên hoang sơ và các khu di tích lịch sử, văn hóa gắn liền với sự hình thành và phát triển của phái Trúc Lâm Yên Tử",
    "Hồ_Hoàn_Kiếm": "Hồ Hoàn Kiếm là hồ nước ngọt nằm ở trung tâm của thủ đô Hà Nội, diện tích của hồ là 12 hecta, chiều rộng là 200m và độ sâu từ 1m đến 1,4m. Bao quanh hồ Hoàn Kiếm là các con phố Lê Thái Tổ, phố Đinh Tiên Hoàng, phố Hàng Khay, tượng của vua Lê Thánh Tông, cầu Thê Húc nằm trên hồ, tháp Bút và đền Bà Kiệu nằm cạnh hồ",
    "Văn_Miếu_-_Quốc_Tử_Giám": "Trường đại học đầu tiên của Việt Nam, nơi tôn vinh truyền thống hiếu học.",
    "Chùa_Một_Cột": "Ngôi chùa độc đáo với kiến trúc trên cột đá giữa hồ sen, mang hình dáng đóa sen.",
    "Lăng_Chủ_tịch_Hồ_Chí_Minh": "Nơi an nghỉ của Chủ tịch Hồ Chí Minh, biểu tượng lòng kính yêu của nhân dân.",
    "Phố_cổ_Hà_Nội": "Khu phố lâu đời với nét kiến trúc cổ kính và nhịp sống truyền thống của người Hà Nội.",
    "Thác_Bản_Giốc": "Một trong những thác nước lớn và đẹp nhất Việt Nam, nằm giữa biên giới Việt - Trung.",
    "Hồ_Ba_Bể": "Hồ nước ngọt lớn giữa rừng núi, nằm trong Vườn quốc gia Ba Bể, nổi bật với thiên nhiên nguyên sơ.",
    "Hang_Pác_Bó": "Di tích cách mạng, nơi Bác Hồ từng sống và làm việc khi trở về nước năm 1941.",
    "Chùa_Bái_Đính": "Quần thể chùa lớn nhất Việt Nam với nhiều kỷ lục về kiến trúc và tượng Phật",
    "Tràng_An": "Di sản kép thế giới với hệ thống hang động, sông ngòi và cảnh sắc hùng vĩ.", 
    "Tam_Cốc_-_Bích_Động": "Vịnh Hạ Long trên cạn với hang động xuyên núi và cảnh sắc thơ mộng",
    "Cố_đô_Hoa_Lư": "Kinh đô đầu tiên của nước Đại Cồ Việt, mang đậm dấu ấn lịch sử và văn hóa.",
    "Fansipan": "Nóc nhà Đông Dương với độ cao 3.143m, hấp dẫn dân phượt và du khách yêu thiên nhiên.",
    "Ruộng_bậc_thang_Sa_Pa": "Tuyệt tác lao động của người dân vùng cao, đẹp nhất vào mùa lúa chín vàng.",
    "Chợ_Bắc_Hà": "Chợ phiên lớn nhất vùng Tây Bắc, nổi bật với bản sắc văn hóa dân tộc.",
    "Đèo_Ô_Quy_Hồ": "Một trong “tứ đại đỉnh đèo”, cảnh quan ngoạn mục, kết nối Lai Châu và Lào Cai.",
    "Động_Phong_Nha": "Hang động tuyệt đẹp với nhũ đá kỳ ảo, thuộc Di sản Phong Nha - Kẻ Bàng.",
    "Quảng_trường_Lâm_Viên": "Biểu tượng du lịch của Đà Lạt, nổi bật với khối hoa dã quỳ và hoa atiso khổng lồ.",
    "Động_Thiên_Đường": "Hang động khô dài nhất châu Á, nổi bật với vẻ đẹp tráng lệ và độc đáo.",
    "Cố_đô_Huế": "Kinh đô triều Nguyễn với hệ thống lăng tẩm, cung điện cổ kính, đậm chất hoài cổ.",
    "Lăng_Tự_Đức": "Lăng tẩm mang vẻ đẹp trầm mặc, lãng mạn của vị vua thi sĩ triều Nguyễn.",
    "Sông_Hương": "Dòng sông thơ mộng gắn liền với vẻ đẹp cố đô Huế.",
    "Chùa_Thiên_Mụ": "Ngôi chùa cổ kính bên sông Hương, là biểu tượng tâm linh của Huế.",
    "Bà_Nà_Hills": "Khu du lịch nổi tiếng với Cầu Vàng, khí hậu mát mẻ và kiến trúc châu Âu cổ điển.",
    "Ngũ_Hành_Sơn": "Quần thể núi đá vôi linh thiêng, có nhiều hang động và chùa chiền cổ kính",
    "Phố_cổ_Hội_An": "Di sản văn hóa thế giới với kiến trúc cổ và nền văn hóa giao thoa Á - Âu",
    "Chùa_Cầu": "Cây cầu cổ độc đáo gắn liền với phố cổ Hội An, do người Nhật xây dựng",
    "Thánh_địa_Mỹ_Sơn": "Quần thể di tích Chăm Pa với kiến trúc đền tháp cổ giữa rừng núi.",
    "Vịnh_Lăng_Cô": "Bãi biển cong hình lưỡi liềm tuyệt đẹp nằm dưới chân đèo Hải Vân.",
    "Địa_đạo_Củ_Chi": "Hệ thống hầm ngầm trong lòng đất, minh chứng cho tinh thần chiến đấu kiên cường",
    "Nhà_thờ_Đức_Bà_Sài_Gòn": "Nhà thờ cổ mang phong cách kiến trúc Pháp giữa lòng TP.HCM",
    "Dinh_Độc_Lập": "Di tích lịch sử quan trọng gắn liền với sự kiện giải phóng miền Nam năm 1975",
    "Chợ_Bến_Thành": "Biểu tượng thương mại và du lịch của TP.HCM với đa dạng hàng hóa.",
    "Bưu_điện_Trung_tâm_Sài_Gòn": "Công trình kiến trúc cổ điển kiểu Pháp nổi bật giữa trung tâm thành phố",
    "Chợ_nổi_Cái_Răng": "Chợ trên sông đặc trưng của miền Tây, buôn bán sôi động vào sáng sớm.",
    "Rừng_tràm_Trà_Sư": "Khu rừng ngập nước đẹp như tranh, nổi bật với thảm bèo xanh rì.",
    "Núi_Cấm": "Núi thiêng ở An Giang, là điểm hành hương nổi tiếng của miền Tây Nam Bộ.",
    "Đảo_Phú_Quốc": "Đảo ngọc với biển xanh cát trắng, điểm đến nghỉ dưỡng hàng đầu Việt Nam",
    "Bãi_Sao": "Một trong những bãi biển đẹp nhất Phú Quốc với cát trắng mịn như kem",
    "Đỉnh_Bàn_Cờ": "Điểm cao nhất bán đảo Sơn Trà, nơi có tượng ông Tiên đang đánh cờ giữa mây trời.",
    "Nhà_thờ_lớn_Hà_Nội": "Nhà thờ cổ kính mang đậm dấu ấn kiến trúc Gothic phương Tây.",
    "Công_viên_Thiên_văn_học": "Công viên chủ đề khoa học vũ trụ đầu tiên tại Việt Nam",
    "Lũng_Cú": "Cột cờ Lũng Cú - nơi địa đầu Tổ quốc, biểu tượng thiêng liêng của chủ quyền.",
    "Sơn_Đoòng": "Hang động lớn nhất thế giới, kỳ quan thiên nhiên độc đáo nằm trong Phong Nha - Kẻ Bàng",
    "Hàm_Cá_Mập": "Toà nhà nổi bật với hình dáng hàm cá mập nằm bên hồ Hoàn Kiếm, biểu tượng kiến trúc hiện đại",
    "Nhà_Thờ_Đá": "Nhà thờ cổ Sa Pa được xây dựng bằng đá nguyên khối từ thời Pháp thuộc"
}

# lấy best model
model_path = torch.load("best_model.pth")

# transform 
transform = transforms.Compose([
    transforms.Resize((224,224)), # resize
    transforms.ToTensor() # scale tu [0,255] ve [0, 1], chuyen anh PIl or numpy array sang tensor pytorch
])

train_set = datasets.ImageFolder("D:/REAL PROJECT/dataset/train", transform=transform)
# lấy classes
places = train_set.classes

# lấy link ảnh cần predict
img_path = "D:/REAL PROJECT/chobenthanh.jpg"


# GỌI MODEL RESNET18
model = models.resnet18(pretrained=False) # ko cần lấy pretrain, lấy weight từ bestmodel.pth 
model.fc = nn.Linear(model.fc.in_features, 48) # thay lớp fc cuối
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# PREDICT
def predict(img_path):
    input_tensor = transform(img_path).unsqueeze(0) # (1, 3, 224, 224)
    
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
    
    predicted_place = places[predicted.item()]
    info = landmark_info[predicted_place]
    origin_path = os.path.join("D:/REAL PROJECT/dataset/train", predicted_place)
    origin_img_name = os.listdir(origin_path)[0]
    origin_img_path = os.path.join(origin_path, origin_img_name)
    origin_img = Image.open(origin_img_path).convert("RGB")
    return predicted_place, info, origin_img


if __name__ == "__main__":
    # Gradio interface
    demo = gr.Interface(
        fn=predict,
        inputs=gr.Image(type="pil"),
        outputs=[gr.Textbox(label="Tên địa danh"), gr.Textbox(label="Mô tả"), gr.Image(type="pil")],
        title="Nhận diện các địa danh của Việt Nam từ ảnh tải lên",
        description="Tải ảnh lên và hệ thống sẽ dự đoán địa danh tương ứng"
    )

    demo.launch()