import os
import cv2 
import pytesseract

path = 'placas'
#path = 'rtsp://admin:123456@10.3.0.122:554/play1.sdp', cv2.CAP_FFMPEG
output = 'list_ocr_text.txt'

class OCR:
    def __init__(self):
        self.list_ocr_text = []

    def iniciar(self):
        self.procurar_imagens()
        self.salvar_lista()

    def procurar_imagens(self):
        for image_name in os.listdir('placas'):
            image_path = os.path.join('placas', image_name)
            if image_name.endswith('.jpg') or image_name.endswith('.png'):
                try:
                    img = self.abrir_imagem(image_path)
                    ocr_text = self.realizar_ocr(img)
                    self.list_ocr_text.append((image_name, ocr_text))
                    self.exibir_imagem(img)
                except Exception as e:
                    print(f'Erro ao processar a imagem "{image_name}": {str(e)}')

    def abrir_imagem(self,img_path):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        return img

    def exibir_imagem(self, img):
        while True:
            cv2.imshow('Imagem', img)
            key = cv2.waitKey(0) & 0xFF
            if key == 27:  # ESC key
                break
        cv2.destroyAllWindows()

    def realizar_ocr(self, img, lang='eng'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        config = r'--psm 3 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' \
                 f'+lang={lang}'

        dpi = 300
        text = pytesseract.image_to_string(thresh, config=config, lang=lang, output_type=pytesseract.Output.DICT)
                                             #,config_psms=pytesseract.PSM.AUTO_OSD)

        return text

    def salvar_lista(self):
        with open(output, 'w') as file:
            for image_item, ocr_text in self.list_ocr_text:
                linha = f'{image_item}\t{ocr_text}\n'
                file.write(linha)

ocr = OCR()
ocr.iniciar()


