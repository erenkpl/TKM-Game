# Gerekli kütüphaneleri import ediyoruz.
import cv2
import mediapipe as mp
import math
import time
import random

kamera = cv2.VideoCapture(0)  # Kameradan görüntü almaya başladık
mpEl = mp.solutions.hands  # MediaPipe kütüphanesinden el tanılama modülünü alıyoruz.
el = mpEl.Hands()  # MediaPipe kütüphanesinden el objectini alıyoruz.

hareketler = ["TAS", "KAGIT", "MAKAS"]  # Oyundaki hareketleri bir listede topladık.

# Gerekli variable'ları initialize ettik.
count = 0
count_oyun = 0
winner = ""
durum = ""
player_score = 0
cpu_score = 0

x0 = 0
y0 = 0

x4 = 0
y4 = 0

x8 = 0
y8 = 0

x12 = 0
y12 = 0

x16 = 0
y16 = 0

x20 = 0
y20 = 0


# Bu fonksiyonda, her bir parmağın ucundaki noktanın avuç içinin en uç noktasına olan uzaklığının koordinatını alıp,
# bu noktalardan pisagor yöntemiyle, arasındaki net mesafeyi buluyoruz.
def finger_coordinates(x, y, xi, yi):
    sumx = abs(x) - abs(xi)
    sumy = abs(y) - abs(yi)
    sumofxy = math.sqrt((sumx * sumx) + (sumy * sumy))
    return sumofxy


# Bu fonksiyonda, oyuncunun ve bilgisayarın yaptığı hareketleri kontrol ediyoruz, ve bu hareketlere göre kazananı
# belirleyip, puan ekliyoruz.
def durum_kontrol():
    global winner
    mevcut_hareket = random.choice(hareketler)
    if durum == mevcut_hareket:
        print("ESIT")
        winner = "Esit"
    elif durum == "KAGIT":
        if mevcut_hareket == "TAS":
            print("Player Wins")
            winner = "Player"
        else:
            print("CPU Wins")
            winner = "CPU"
    elif durum == "TAS":
        if mevcut_hareket == "MAKAS":
            print("Player Wins")
            winner = "Player"
        else:
            print("CPU Wins")
            winner = "CPU"
    elif durum == "MAKAS":
        if mevcut_hareket == "KAGIT":
            print("Player Wins")
            winner = "Player"
        else:
            print("CPU Wins")
            winner = "CPU"


while True:
    cap, img = kamera.read()  # Kameradan gelen görüntüleri cap ve img isimli variable'lara aktardık.
    imgToRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    sonuc = el.process(imgToRGB)  # Kameradan gelen görüntüdeki elleri algılayabilmesi için el objectine gönderdik
    if durum == "":
        if count_oyun > 0:
            time.sleep(1)  # Oyun sonuçlandığında yeni ekrana geçmeden kazananın görüntülenmesi için durduruyoruz.
            count_oyun = 0
        cv2.putText(img, "Tas-Kagit-Makas Oyununa Hosgeldiniz", (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 150), 2)
        cv2.putText(img,
                    "Elinizi Kameraya 20-25 cm Mesafede Tutunuz.", (10, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 150), 2)
        cv2.putText(img, "Baslamak icin tamam isareti yapiniz", (10, 130), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 150), 2)
    if sonuc.multi_hand_landmarks:
        for handlms in sonuc.multi_hand_landmarks:  # Görüntüdeki eller içinden,
            for id, lm in enumerate(handlms.landmark):  # Her bir noktayı ayrı ayrı alıyoruz.
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 4:  # Başparmak ucu koordinatı
                    x4 = cx
                    y4 = cy

                if id == 8:  # İşaret parmağı ucu koordinatı
                    x8 = cx
                    y8 = cy

                if id == 12:  # Orta parmak ucu koordinatı
                    x12 = cx
                    y12 = cy

                if id == 16:  # Yüzük parmağı ucu koordinatı
                    x16 = cx
                    y16 = cy

                if id == 20:  # Serçe parmağı ucu koordinatı
                    x20 = cx
                    y20 = cy

                if id == 0:  # Avuç içi koordinatı
                    x0 = cx
                    y0 = cy

                # Her bir parmak ucunun, avuç içine olan uzaklığını hesaplamak için fonksiyonumuza gönderdik.
                sumofxy4 = finger_coordinates(x4, y4, x0, y0)
                sumofxy8 = finger_coordinates(x8, y8, x0, y0)
                sumofxy12 = finger_coordinates(x12, y12, x0, y0)
                sumofxy16 = finger_coordinates(x16, y16, x0, y0)
                sumofxy20 = finger_coordinates(x20, y20, x0, y0)

                if durum == "":  # Oyuna başlamak için elimizle "Tamam" işareti vermemiz gerekiyor.
                    if sumofxy4 > 210 and ((sumofxy8 < 170 and sumofxy12 < 170) and
                                           (sumofxy16 < 160 and sumofxy20 < 150)):
                        cv2.putText(img, "TAMAM", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                    (0, 0, 150), 3)
                        durum = "TAMAM"
                        count = 0
                        start_time = time.time()  # Hareket için gerekli saniyeyi tutmak için başladığımız zamanı aldık.
                else:  # Oyuna başladıktan sonra yaptığımız hareketi parmağın avuç içine uzaklığına göre tanımlıyoruz.
                    cv2.putText(img, "3 Saniye icinde hareketinizi secin.", (10, 150), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 150), 3)
                    if (sumofxy8 > 200 and sumofxy12 > 200) and (sumofxy16 > 180 and sumofxy20 > 150):
                        cv2.putText(img, "KAGIT", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 150), 3)
                        durum = "KAGIT"
                    elif sumofxy8 > 200 and sumofxy12 > 180:
                        cv2.putText(img, "MAKAS", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 150), 3)
                        durum = "MAKAS"
                    elif (sumofxy8 < 190 and sumofxy12 < 180) and (sumofxy16 < 180 and sumofxy20 < 180):
                        cv2.putText(img, "TAS", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 150), 3)
                        durum = "TAS"
                    end_time = time.time()  # Gerekli saniyeyi hesaplamak için bitiş süresini alıyoruz.
                    #  Süre 3 saniyeden fazla olunca turu bitirip kazananı belirliyoruz.
                    if end_time - start_time > 3:
                        if count == 0:
                            durum_kontrol()
                            count += 1
                            count_oyun += 1
                            durum = ""
                            if winner == "Player":
                                player_score += 1
                            elif winner == "CPU":
                                cpu_score += 1
                        cv2.putText(img, ("Kazanan: " + winner), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 150), 3)
                        cv2.putText(img, ("Player: " + str(player_score)), (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 150, 150), 2)
                        cv2.putText(img, ("CPU: " + str(cpu_score)), (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 150, 150), 2)

    cv2.imshow("TKM", img)
    if cv2.waitKey(2) == 27:  # Oyundan, klavyedeki "ESC" tuşuna basarak çıkabilmemiz için kondisyon tanımladık.
        break

# Oyun bitince kamerayı ve tüm pencereleri kapatıyoruz.
kamera.release()
cv2.destroyAllWindows()
