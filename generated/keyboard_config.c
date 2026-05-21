// 自动生成，请勿手动修改
// 生成时间: 2026-05-21 22:18:47

#pragma once

// ========== 设备信息 ==========
#define VENDOR_ID       0xFEED
#define PRODUCT_ID      0x6060
#define DEVICE_VER      0x0100
#define MANUFACTURER    CUSTOM_KEYBOARD
#define PRODUCT         CUSTOM_KEYBOARD

#define BLUETOOTH_NAME  "BT_KB"


// ========== 矩阵配置 ==========
#define MATRIX_ROWS     6
#define MATRIX_COLS     14

// ========== RGB 配置 ==========
#define RGB_TOTAL_LEDS  41
#define RGB_MAX_BRIGHTNESS 255
#define RGB_BRIGHTNESS_STEPS 5
#define RGB_SPEED_STEPS 5

// ========== 按键映射（四层） ==========
// 注意：KC_NO 表示无动作
typedef uint16_t keycode_t;

// 矩阵键值表 [layer][row][col]
extern const keycode_t keymaps[][MATRIX_ROWS][MATRIX_COLS];

const keycode_t keymaps[][MATRIX_ROWS][MATRIX_COLS] = { 
    [0] = LAYOUT_tkl_ansi(  
         KC_ESC    , KC_1      , KC_2      , KC_3      , KC_4      , KC_5      , KC_6      , KC_7      , KC_8      , KC_9      , KC_0      ,     
         KC_Q      , KC_W      , KC_E      , KC_R      , KC_T      , KC_Y      , KC_U      , KC_I      , KC_O      , KC_P      ,     
         KC_A      , KC_S      , KC_D      , KC_F      , KC_G      , KC_H      , KC_J      , KC_K      , KC_L      , KC_SPACE  ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO        
    ), 
    [1] = LAYOUT_tkl_ansi(  
         KC_GRV    , KC_F1     , KC_F2     , KC_F3     , KC_F4     , KC_F5     , KC_F6     , KC_F7     , KC_F8     , KC_F9     , KC_F10    ,     
         KC_1      , KC_2      , KC_3      , KC_4      , KC_5      , KC_6      , KC_7      , KC_8      , KC_9      , KC_0      ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_ENTER  ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO        
    ), 
    [2] = LAYOUT_tkl_ansi(  
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO        
    ), 
    [3] = LAYOUT_tkl_ansi(  
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     ,     
         KC_NO     , KC_NO     , KC_NO     , KC_NO        
    )
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    
    [0] = LAYOUT_tkl_ansi(
        KC_ESC,           KC_F1,   KC_F2,     KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,             KC_F13,   KC_HOME,  KC_INS,  KC_DEL,   KC_END,  
        KC_GRV,  KC_1,    KC_2,    KC_3,      KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,  KC_EQL,   KC_BSPC,            KC_PGUP,  KC_NUM,   KC_PSLS, KC_PAST,  KC_PMNS,
        KC_TAB,  KC_Q,    KC_W,    KC_E,      KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,  KC_BSLS,            KC_PGDN,  KC_P7,    KC_P8,   KC_P9,    KC_PPLS,
        KC_CAPS, KC_A,    KC_S,    KC_D,      KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,  KC_K42,   KC_ENT ,  KC_ENT ,  KC_PSCR,  KC_P4,    KC_P5,   KC_P6,
        KC_LSFT,          KC_Z,    KC_X,      KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,  KC_RSFT,  KC_UP ,                       KC_P1,    KC_P2,   KC_P3,
        KC_LCTL, KC_LGUI, KC_LALT,                      KC_SPC,                                 KC_RALT,  MO(2),              KC_LEFT,  KC_DOWN,  KC_RGHT,            KC_P0,    KC_PDOT, KC_PENT 
    ),
    [1] = LAYOUT_tkl_ansi(
        KC_ESC,           KC_BRID, KC_BRIU,   C(KC_UP), G(KC_F),  IOS_SIRI, LSG(KC_4),KC_MPRV,  KC_MPLY,  KC_MNXT,  KC_MUTE,  KC_VOLD,  KC_VOLU,            KC_F13,   KC_HOME,  KC_INS,  KC_DEL,   KC_END,
        KC_GRV,  KC_1,    KC_2,    KC_3,      KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,  KC_EQL,   KC_BSPC,            KC_PGUP,  KC_NUM,   KC_PSLS, KC_PAST,  KC_PMNS,
        KC_TAB,  KC_Q,    KC_W,    KC_E,      KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,  KC_BSLS,            KC_PGDN,  KC_P7,    KC_P8,   KC_P9,    KC_PPLS,
        KC_CAPS, KC_A,    KC_S,    KC_D,      KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,  KC_K42,   KC_ENT ,  KC_ENT ,  KC_PSCR,  KC_P4,    KC_P5,   KC_P6,
        KC_LSFT,          KC_Z,    KC_X,      KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,  KC_RSFT,  KC_UP ,                       KC_P1,    KC_P2,   KC_P3,
        KC_LCTL, KC_LALT, KC_LGUI,                      KC_SPC,                                 KC_RGUI,  MO(3),              KC_LEFT,  KC_DOWN,  KC_RGHT,            KC_P0,    KC_PDOT, KC_PENT 
    ), 
    [2] = LAYOUT_tkl_ansi( 
        KC_ESC,           KC_BRID, KC_BRIU,   KC_WHOM,  KC_MAIL,  KC_CALC,  KC_MSEL,  KC_MPRV,  KC_MPLY,  KC_MNXT,  KC_MUTE,  KC_VOLD,  KC_VOLU,            KC_F13,   KC_HOME,  KC_INS,  KC_DEL,   KC_END, 
        KC_GRV,  MD_BLE1, MD_BLE2, MD_BLE3,   MD_24G,   MD_USB,   KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     RGB_SPD,  RGB_SPI,  U_EE_CLR,           KC_PGUP,  KC_NUM,   KC_PSLS, KC_PAST,  KC_PMNS,
        SIDE_HUI,KC_Q,    KC_W,    KC_E,      KC_R,     TIME_ST,  KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,  RGB_MOD,            L_LOOP,   KC_P7,    KC_P8,   KC_P9,    KC_PPLS,
        KC_CAPS, TO(0),   TO(1),   KC_D,      KC_F,     KC_G,     QK_DEB,   KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,  RGB_MOD,  RGB_RTOG, RGB_RTOG, KC_PSCR,  KC_P4,    KC_P5,   KC_P6,
        KC_LSFT,          KC_Z,    KC_X,      KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     SIDE_VAD, SIDE_VAI, SIDE_MOD, KC_RSFT,  RGB_VAI,                      KC_P1,    KC_P2,   KC_P3,
        TEST_CL, QK_WLO,  KC_LALT,                      KC_SPC,                                 KC_RALT,  KC_NO,              RGB_HUD,  RGB_VAD,  RGB_HUI,            KC_P0,    KC_PDOT, KC_PENT 
    ), 
    [3] = LAYOUT_tkl_ansi( 
        KC_ESC,           KC_F1,   KC_F2,     KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,             KC_F13,   KC_HOME,  KC_INS,  KC_DEL,   KC_END, 
        KC_GRV,  MD_BLE1, MD_BLE2, MD_BLE3,   MD_24G,   MD_USB,   KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     RGB_SPD,  RGB_SPI,  U_EE_CLR,           KC_PGUP,  KC_NUM,   KC_PSLS, KC_PAST,  KC_PMNS,
        SIDE_HUI,KC_Q,    KC_W,    KC_E,      KC_R,     TIME_ST,  KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,  RGB_MOD,            L_LOOP,   KC_P7,    KC_P8,   KC_P9,    KC_PPLS,
        KC_CAPS, TO(0),   TO(1),   KC_D,      KC_F,     KC_G,     QK_DEB,   KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,  RGB_MOD,  RGB_RTOG, RGB_RTOG, KC_PSCR,  KC_P4,    KC_P5,   KC_P6,
        KC_LSFT,          KC_Z,    KC_X,      KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     SIDE_VAD, SIDE_VAI, SIDE_MOD, KC_RSFT,  RGB_VAI,                      KC_P1,    KC_P2,   KC_P3,
        TEST_CL, KC_LALT, KC_LGUI,                      KC_SPC,                                 KC_RGUI,  KC_NO,              RGB_HUD,  RGB_VAD,  RGB_HUI,            KC_P0,    KC_PDOT, KC_PENT 
    )
};

// LED 矩阵位置映射（矩阵行列 -> LED 索引）
// 尺寸: MATRIX_ROWS x MATRIX_COLS
led_config_t g_led_config = { {
    {      0,      1,      2,      3,      4,      5,      6,      7,      8,      9,     10, NO_LED, NO_LED, NO_LED }, 
    {     11,     12,     13,     14,     15,     16,     17,     18,     19,     20, NO_LED, NO_LED, NO_LED, NO_LED }, 
    {     21,     22,     23,     24,     25,     26,     27,     28,     29,     30, NO_LED, NO_LED, NO_LED, NO_LED }, 
    {     32,     33,     34, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED }, 
    {     35,     36, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED }, 
    { NO_LED,     37,     38,     39,     40, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED }
}, {
    {   0,   0 }, {  10,   0 }, {  20,   0 }, {  30,   0 }, {  40,   0 }, {  50,   0 }, {  60,   0 }, {  70,   0 }, {  80,   0 }, {  90,   0 }, { 100,   0 },
    {   0,  10 }, {  10,  10 }, {  20,  10 }, {  30,  10 }, {  40,  10 }, {  50,  10 }, {  60,  10 }, {  70,  10 }, {  80,  10 }, {  90,  10 },
    {   0,  20 }, {  12,  20 }, {  22,  20 }, {  32,  20 }, {  42,  20 }, {  52,  20 }, {  62,  20 }, {  72,  20 }, {  82,  20 }, {  92,  20 },
    {   0,  30 }, {   0,  40 }, {  46,  30 },
    {  56,  30 }, {   0,  50 },
    {  10,  40 }, {  10,  50 }, {  20,  50 }, {  30,  50 }
}, {
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
      1,   1,   1,
      1,   1,
      1,   1,   1,   1
} };

led_config_t g_led_config = { {
    { 0        , 1        , 2        , 3        , 4        , 5        , 6        , 7        , 8        , 9        , 10       , 11       , 12       , 13       , 14       , 15       },
	{ 18       , 19       , 20       , 21       , 22       , 23       , 24       , 25       , 26       , 27       , 28       , 29       , 30       , 31       , 32       , 36       },
	{ 37       , 38       , 39       , 40       , 41       , 42       , 43       , 44       , 45       , 46       , 47       , 48       , 49       , 50       , 51       , 55       },
	{ 56       , 57       , 58       , 59       , 60       , 61       , 62       , 63       , 64       , 65       , 66       , 67       , 68       , 69       , 70       , NO_LED   },
	{ 74       , 75       , 76       , 77       , 78       , 79       , 80       , 81       , 82       , 83       , 84       , 85       , 86       , 50       , NO_LED   , NO_LED   },
	{ 91       , 92       , 93       , 16       , 17       , 94       , NO_LED   , NO_LED   , NO_LED   , 95       , 96       , 97       , 98       , 99       , NO_LED   , NO_LED   },
    { 33       , 34       , 35       , 52       , 53       , 54       , 71       , 72       , 73       , 87       , 88       , 89       , 100      , 101      , 90       , NO_LED   }
},{
    { 0,  10},             { 20, 10}, { 30, 10}, { 40, 10}, { 50, 10}, { 68, 10}, { 78, 10}, { 88, 10}, { 98,  10}, { 116, 10}, { 126, 10}, { 136, 10}, { 146, 10},             { 161, 10}, { 176, 10}, { 186, 10}, { 196, 10}, { 206, 10},                        
    { 0,  20},  { 10, 20}, { 20, 20}, { 31, 20}, { 41, 20}, { 52, 20}, { 62, 20}, { 72, 20}, { 83, 20}, { 93,  20}, { 103, 20}, { 116, 20}, { 126, 20}, { 141, 20},             { 161, 20}, { 176, 20}, { 186, 20}, { 196, 20}, { 206, 20},           
    { 4,  30},  { 15, 30}, { 25, 30}, { 35, 30}, { 45, 30}, { 56, 30}, { 66, 30}, { 76, 30}, { 86, 30}, { 97,  30}, { 107, 30}, { 117, 30}, { 131, 30},             { 143, 30}, { 161, 30}, { 176, 30}, { 186, 30}, { 196, 30}, { 206, 35},
    { 6,  40},  { 17, 40}, { 27, 40}, { 37, 40}, { 47, 40}, { 58, 40}, { 68, 40}, { 78, 40}, { 88, 40}, { 99,  40}, { 109, 40}, { 119, 40}, { 129, 40}, { 140, 40},             { 161, 40}, { 176, 40}, { 186, 40}, { 196, 40}, 
    { 8,  50},             { 23, 50}, { 33, 50}, { 43, 50}, { 53, 50}, { 64, 50}, { 74, 50}, { 84, 50}, { 97,  50}, { 107, 50}, { 117, 50},             { 132, 50}, { 147, 50},             { 176, 50}, { 186, 50}, { 196, 50}, { 206, 55},
    { 0,  60},  { 14, 60}, { 26, 60},                       { 65, 60},                                  { 103, 60}, { 120, 60},                         { 136, 60}, { 147, 60}, { 159, 60},             { 186, 60}, { 196, 60}, 

    { 255,65}, { 255,65}, { 255,65}, { 255,65},

    { 255,65}, { 255,65}, { 255,65}, 
    { 255,65}, { 255,65}, { 255,65}
}, {
    1,      1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,      1,  1,  1,  1,  1,      
    1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,      1,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,      1,  1,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,      1,  1,  1,  1,  
    1,      1,  1,  1,  1,  1,  1,  1,  1,  1,  1,      1,  1,      1,  1,  1,  1,
    1,  1,  1,          1,              1,  1,          1,  1,  1,      1,  1,  

    0,  0,  0,  0,

    0,  0,  0,
    0,  0,  0
} };