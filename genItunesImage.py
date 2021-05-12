import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import argparse
import sys
import os.path


def get_args():
    # 準備
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="please set me", type=str)

    parser.add_argument("--order", "--size", "-s",
                        type=int, default=5, help="order of size")
    parser.add_argument("--isRawText", "-r", action="store_true",
                        help="whether input is raw text not file name")

    # 結果を受ける
    args = parser.parse_args()
    return args


def genCodeImage(text="No Input", order=5):

    ttfontname = "font/Scancardium_2.0.ttf"
    fontsize = 25*order
    margin = (25*order, 25*order)
    frame_width = 4*order

    # generate font image
    font = PIL.ImageFont.truetype(ttfontname, fontsize)
    # textWidth, textHeight

    def obtainTextSize(text="NoInput", font=False):
        if font is False:
            return (0, 0)
        canvasTmp = PIL.Image.new('RGB', (300, 100), (255, 255, 255))
        drawTmp = PIL.ImageDraw.Draw(canvasTmp)
        return drawTmp.textsize(text, font=font)

    textSize = obtainTextSize(text=text, font=font)

    # 画像サイズ，背景色，フォントの色を決定
    canvasSize = [textSize[ind]+margin[ind]*2+frame_width for ind in range(2)]
    backgroundRGB = (255, 255, 255)
    textRGB = (0, 0, 0)

    # 文字を描く画像の作成
    canvas = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(canvas)

    # draw frame
    canvas.widthTmp = canvas.width
    canvas.heightTmp = canvas.height
    canvas.zero = 0

    frame_edges = [[canvas.zero if num in [1, 2] else canvas.widthTmp,
                    canvas.zero if num in [2, 3] else canvas.heightTmp] for num in range(4)]
    frame_coors = [frame_edges[num] +
                   frame_edges[(num+1) % 4] for num in range(4)]
    for coor in frame_coors:
        draw.line(coor, fill=(0, 0, 0), width=frame_width)

    # draw font
    textTopLeft = (margin[0]+frame_width/2, margin[1]+frame_width/2)
    draw.text(textTopLeft, text, fill=textRGB, font=font)
    return canvas


if __name__ == "__main__":
    args = get_args()

    def obtainRawTexts(args):
        isPipe = not sys.stdin.isatty()
        if isPipe:
            return [s.strip() for s in sys.stdin.readlines()]
        elif args.isRawText:
            return args.input
        else:
            filename = args.input
            if not os.path.isfile(filename):
                return ["Not Exist"]
            with open(filename) as f:
                return f.readlines()

    texts = obtainRawTexts(args)
    for textTmp in texts:
        text="".join(textTmp.splitlines())
        canvas = genCodeImage(text="".join(text.splitlines()), order=args.order)
        canvas.save(f"img/{text}.png")
