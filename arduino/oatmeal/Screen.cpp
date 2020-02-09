#include "Screen.h"

#define BLACK    0x0000
#define BLUE     0x001F
#define RED      0xF800
#define GREEN    0x07E0
#define CYAN     0x07FF
#define MAGENTA  0xF81F
#define YELLOW   0xFFE0
#define WHITE    0xFFFF

#define WIDTH   128
#define HEIGHT  128
#define CS_PIN  50
#define DC_PIN  49
#define SDA_PIN 47
#define SCL_PIN 46
#define RES_PIN 48

#define BGND_COLOR  BLACK
#define TEMP_COLOR  MAGENTA
#define HUMID_COLOR WHITE

#define YOFF       32
#define TEXT_XOFF  15
#define TEXT_YOFF  5
#define HUMID_YOFF 80

namespace {

const int gy = (HEIGHT + YOFF) / 2;
const int gx[] = {WIDTH/4, WIDTH/4 * 3};

void printFloat(char* buf, float f) {
  const unsigned int i = f * 100;
  const unsigned int whole = i / 100;
  const unsigned int decimal = i % 100;
  sprintf(buf, "%d.%d", whole, decimal);
}

uint16_t makeRGB(uint8_t r, uint8_t g, uint8_t b) {
  const uint16_t red = r / 8;
  const uint16_t green = g / 4;
  const uint16_t blue = b  / 8;
  const uint16_t c = (red << 11) | (green << 5) | blue;
  return c;
}

struct Color {
  uint8_t r, g, b;
  Color() : r(0), g(0), b(0) {}
  Color(uint8_t r, uint8_t g, uint8_t b) : r(r), g(g), b(b) {}
  uint16_t rgb() {
    return makeRGB(r, g, b);
  }
};

void drawArc(Adafruit_SSD1351& screen, int cx, int cy, int r, int sa, int fa, const Color& startColor, const Color& endColor) {
  const float range = (sa < fa) ? (fa-sa) : (360-sa+fa);
  const int pc = 2 * PI * r * r * range / 360.0f;
  const float fpc = static_cast<float>(pc);
  const float angleOffset = static_cast<float>(sa) / 180.f * PI;
  const float radius = r;

  const float dR = (static_cast<float>(endColor.r) - static_cast<float>(startColor.r)) / fpc;
  const float dG = (static_cast<float>(endColor.g) - static_cast<float>(startColor.g)) / fpc;
  const float dB = (static_cast<float>(endColor.b) - static_cast<float>(startColor.b)) / fpc;

  screen.startWrite();
  for (int i = 0; i<pc; ++i) {
    const float p = static_cast<float>(i) / fpc;
    const float a = range * p * PI / 180.0f + angleOffset;
    const int x = round(cos(a) * radius) + cx;
    const int y = round(sin(a) * radius) + cy;
    screen.writePixel(x, y, makeRGB(startColor.r + dR*i, startColor.g + dG*i, startColor.b + dB*i));
  }
  screen.endWrite();
}

void drawCircle(Adafruit_SSD1351& screen, int cx, int cy, int r, const Color& color) {
  drawArc(screen, cx, cy, r, 0, 360, color, color);
}

void drawLine(Adafruit_SSD1351& screen, int cx, int cy, int a, int l, uint16_t color) {
  const float angle = static_cast<float>(a) * PI / 180.0f;
  const float xfactor = cos(angle);
  const float yfactor = sin(angle);

  screen.startWrite();
  for (int i = 0; i<l; ++i) {
    const float fi = static_cast<float>(i);
    const int x = round(fi * xfactor) + cx;
    const int y = round(fi * yfactor) + cy;
    screen.writePixel(x, y, color);
  }
  screen.endWrite();
}
}

Screen::Screen()
: screen(WIDTH, HEIGHT, CS_PIN, DC_PIN, SDA_PIN, SCL_PIN, RES_PIN) {
  memset(temp, 0, sizeof(temp));
  memset(humid, 0, sizeof(humid));
  angle[0] = angle[1] = 90;
}

void Screen::init() {
  screen.begin();
  
  screen.setFont();
  screen.fillScreen(BGND_COLOR);
  screen.setTextSize(1);

  screen.startWrite();
  screen.writeFastHLine(0, YOFF, WIDTH/2, RED);
  screen.writeFastHLine(0, YOFF+95, WIDTH/2, RED);
  screen.writeFastVLine(0, YOFF, HEIGHT, RED);
  screen.writeFastVLine(WIDTH/2, YOFF, HEIGHT, RED);
  
  screen.writeFastHLine(WIDTH/2+1, YOFF, WIDTH/2, BLUE);
  screen.writeFastHLine(WIDTH/2+1, YOFF+95, WIDTH/2, BLUE);
  screen.writeFastVLine(WIDTH-1, YOFF, HEIGHT, BLUE);
  screen.writeFastVLine(WIDTH/2+1, YOFF, HEIGHT, BLUE);
  screen.endWrite();

  drawArc(screen, gx[0], gy, 20, 135, 270, Color(255, 0, 0), Color(0, 255, 0));
  drawArc(screen, gx[0], gy, 20, 270, 45, Color(0, 255, 0), Color(255, 0, 0));
  drawArc(screen, gx[0], gy, 20, 45, 135, Color(255, 255, 255), Color(255, 255, 255));
  
  drawArc(screen, gx[1], gy, 20, 135, 270, Color(255, 0, 0), Color(0, 255, 0));
  drawArc(screen, gx[1], gy, 20, 270, 45, Color(0, 255, 0), Color(255, 0, 0));
  drawArc(screen, gx[1], gy, 20, 45, 135, Color(255, 255, 255), Color(255, 255, 255));
}

void Screen::updateReading(unsigned int i, float t, float h) {
  const int bx = (i == 0) ? 0 : 64;
  char buf[32];
  char fbuf[8];

  printFloat(fbuf, t);
  sprintf(buf, "%sF", fbuf);
  if (strcmp(buf, temp[i]) != 0) {
    screen.setCursor(bx + TEXT_XOFF, TEXT_YOFF + YOFF);
    screen.setTextColor(BGND_COLOR);
    screen.print(temp[i]);
    strcpy(temp[i], buf);
    screen.setCursor(bx + TEXT_XOFF, TEXT_YOFF + YOFF);
    screen.setTextColor(TEMP_COLOR);
    screen.print(temp[i]);
  }

  const int a = (map(round(t), 60, 85, 90, 360) + 45) % 360;
  if (a != angle[i]) {
    drawLine(screen, gx[i], gy, angle[i], 18, BGND_COLOR);
    angle[i] = a;
    const uint16_t r = t < 75 ?
            map(round(t), 60, 75, 255, 0) :
            map(round(t), 75, 90, 255, 0);
    drawLine(screen, gx[i], gy, angle[i], 18, makeRGB(r, 255-r, 0));
  }

  printFloat(fbuf, h);
  sprintf(buf, "%s%%", fbuf);
  if (strcmp(buf, humid[i]) != 0) {
    screen.setCursor(bx + TEXT_XOFF, TEXT_YOFF + HUMID_YOFF + YOFF);
    screen.setTextColor(BGND_COLOR);
    screen.print(humid[i]);
    strcpy(humid[i], buf);
    screen.setCursor(bx + TEXT_XOFF, TEXT_YOFF + HUMID_YOFF + YOFF);
    screen.setTextColor(HUMID_COLOR);
    screen.print(humid[i]);
  }
}
