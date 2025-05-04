from PIL import Image, ImageDraw
from ToaDoTungMuc import KhuVucSBD, KhuVucMaDeThi, Phan_1, Phan_2, Phan_3
  
# -------------------------------------------------------------------
'''
SO BAO DANH
'''
def XacDinhSBD(image):
    print("SBD cua ban: ", end="")
    for i, PhanTraLoi in enumerate(KhuVucSBD):
        TraLoi = XacDinhTraLoi(image, PhanTraLoi)
        print(f"{TraLoi}", end="")
    print("")

# -------------------------------------------------------------------
'''
MA DE THI
'''
def XacDinhMaDeThi(image):
    print("Ma De Thi cua ban: ", end="")
    for i, PhanTraLoi in enumerate(KhuVucMaDeThi):
        TraLoi = XacDinhTraLoi(image, PhanTraLoi)
        print(f"{TraLoi}", end="")
    print("")

# -------------------------------------------------------------------
'''
PHAN 1
'''
def XacDinhPhanTraLoi1(image):
    print("Phan 1:")
    for i, PhanTraLoi in enumerate(Phan_1):
        TraLoi = XacDinhTraLoi(image, PhanTraLoi)
        print(f"{i+1}{TraLoi}", end=" ")
    print("")

# -------------------------------------------------------------------
'''
PHAN 2
'''
def XacDinhPhanTraLoi2(image):
    print("Phan 2")
    Phan_2_Cau1234  = ['Cau 1', 'Cau 2', 'Cau 3', 'Cau 4']
    Phan_2_abcd     = ['a', 'b', 'c', 'd']
    for i, PhanTraLoi in enumerate(Phan_2):
        Temp_1234 = i //4
        Temp_abcd = i % 4

        if Temp_1234 >= len(Phan_2_Cau1234):
            break

        TraLoi = XacDinhTraLoi(image, PhanTraLoi)
        print(f"{Phan_2_Cau1234[Temp_1234]}{Phan_2_abcd[Temp_abcd]}: {TraLoi}", end="\t")
        if Temp_abcd == 3: print()
    print("")

# -------------------------------------------------------------------
'''
PHAN 3
'''
def XacDinhPhanTraLoi3(image):
    print("Phan 3")
    Nhan = [1, 10, 100, 1000]
    HeSoNhan = 0
    KetQua = 0
    for i, CauHoi_Phan3 in enumerate(Phan_3):
        KetQua = 0
        HeSoNhan = 0
        for j, PhanTraLoi in enumerate(CauHoi_Phan3[1:], start=1):
            TraLoi = XacDinhTraLoi(image, PhanTraLoi)
            if TraLoi is not None:
                KetQua += int(TraLoi) * Nhan[HeSoNhan]
                HeSoNhan = HeSoNhan + 1
        for k, PhanTraLoi in enumerate(CauHoi_Phan3[0]):
            KhuVucCat = image.crop(PhanTraLoi)
            draw = ImageDraw.Draw(image)
            draw.rectangle(PhanTraLoi, outline="red", width=2)
            if ToDam(KhuVucCat):
                if k == 0:
                    KetQua = -KetQua
                if k == 1:
                    KetQua /= 100;
                if k == 2:
                    KetQua /= 10;
        print(f"Cau {i+1}: {KetQua}")

# -------------------------------------------------------------------
'''
TRA LOI TRAC NGHIEM
'''
def XacDinhTraLoi(image, PhanTraLoi):
    DemSoVung = len(PhanTraLoi)
    Temp3 = []
    if DemSoVung == 2:
        Temp3 = ['Dung', 'Sai']
    elif DemSoVung == 4:
        Temp3 = ['A', 'B', 'C', 'D']
    elif DemSoVung == 10:
        Temp3 = [str(i) for i in range(10)]
    else:
        return None
    for i, Cat in enumerate(PhanTraLoi):
        KhuVucCat = image.crop(Cat)
        draw = ImageDraw.Draw(image)
        draw.rectangle(Cat, outline="red", width=2)
        if ToDam(KhuVucCat):
            return Temp3[i]
    return None

# -------------------------------------------------------------------
'''
TO DAM
'''
def ToDam(todam_image):
    gray_image = todam_image.convert("L")
    threshold_value = 200
    binary_image = gray_image.point(lambda p: p > threshold_value and 255)
    avg_pixel_value = sum(binary_image.getdata()) / (binary_image.width * binary_image.height)
    return avg_pixel_value < 200

# -------------------------------------------------------------------
def main():
    image_path = r"E:\Computer Vision\CuoiKyProject\21200274\BaiLamTracNghiem.jpg"
    image = Image.open(image_path)

    XacDinhSBD(image)
    XacDinhMaDeThi(image)
    XacDinhPhanTraLoi1(image)
    XacDinhPhanTraLoi2(image)
    XacDinhPhanTraLoi3(image)

# Chay chuong trinh
if __name__ == "__main__":
    main()