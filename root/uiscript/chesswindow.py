import uiScriptLocale

MAIN_WIDTH = 640
MAIN_HEIGHT = 480

window = {
	"name" : "ChessWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : MAIN_WIDTH,
	"height" : MAIN_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "window",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : MAIN_WIDTH,
			"height" : MAIN_HEIGHT,

			"children" :
			(
				## Arkaplan Resmi
				{
					"name" : "MainBackground",
					"type" : "expanded_image",
					"x" : 0, "y" : 0,
					"image" : "d:/ymir work/ui/chess/arkaplan.tga",
				},
				## Title (Şeffaf Başlık Alanı)
				{
					"name" : "TitleBar",
					"type" : "window",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : MAIN_WIDTH - 16,
					"height" : 25,

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":(640 - 16)/2, "y":3, "text":"Satranc Sistemi", "text_horizontal_align":"center" },
						{ 
							"name" : "CloseButton", 
							"type" : "button", 
							"x" : 640 - 32, "y" : 0, 
							"default_image" : "d:/ymir work/ui/public/close_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
						},
					),
				},

				## Board Grid (Sol Taraf)
				{
					"name" : "board_grid",
					"type" : "window",

					"x" : 30,
					"y" : 50,

					"width" : 320,
					"height" : 320,
				},

				## Hamle Gecmisi (Sag Ust)
				{
					"name" : "history_panel",
					"type" : "window",
					"x" : 380, "y" : 50,
					"width" : 200, "height" : 120,
					"children" :
					(
						{ "name":"HistoryTitle", "type":"text", "x":10, "y":10, "text":"Hamle Geçmişi", "color":0xffefd587 },
					),
				},

				## Sure Paneli (Sag Alt)
				{
					"name" : "clock_panel",
					"type" : "window",
					"x" : 380, "y" : 180,
					"width" : 200, "height" : 100,
					"children" :
					(
						{ "name":"BlackIcon", "type":"text", "x":40, "y":15, "text":"SİYAH", "text_horizontal_align":"center" },
						{ "name":"WhiteIcon", "type":"text", "x":130, "y":15, "text":"BEYAZ", "text_horizontal_align":"center" },
						{ "name":"BlackTime", "type":"text", "x":40, "y":40, "text":"10:00", "text_horizontal_align":"center" },
						{ "name":"WhiteTime", "type":"text", "x":130, "y":40, "text":"10:00", "text_horizontal_align":"center" },
					),
				},

				## Alt Butonlar ve Kontroller
				{
					"name" : "status_text",
					"type" : "text",
					"x" : 480, "y" : 330,
					"text" : "Beklemede",
					"text_horizontal_align" : "center",
				},

				{
					"name" : "invite_button",
					"type" : "button",
					"x" : 380, "y" : 355,
					"width" : 60, "height" : 25,
					"default_image" : "d:/ymir work/ui/chess/btn_invite.tga",
					"over_image" : "d:/ymir work/ui/chess/btn_invite.tga",
					"down_image" : "d:/ymir work/ui/chess/btn_invite.tga",
				},
				{
					"name" : "bot_button",
					"type" : "button",
					"x" : 450, "y" : 355,
					"width" : 60, "height" : 25,
					"default_image" : "d:/ymir work/ui/chess/btn_bot.tga",
					"over_image" : "d:/ymir work/ui/chess/btn_bot.tga",
					"down_image" : "d:/ymir work/ui/chess/btn_bot.tga",
				},
				{
					"name" : "quit_button",
					"type" : "button",
					"x" : 520, "y" : 355,
					"width" : 60, "height" : 25,
					"default_image" : "d:/ymir work/ui/chess/btn_quit.tga",
					"over_image" : "d:/ymir work/ui/chess/btn_quit.tga",
					"down_image" : "d:/ymir work/ui/chess/btn_quit.tga",
				},

				{
					"name" : "name_slot",
					"type" : "slotbar",
					"x" : 380, "y" : 300,
					"width" : 150, "height" : 18,
					"children" :
					(
						{ "name" : "name_edit", "type" : "editline", "x" : 3, "y" : 3, "width" : 144, "height" : 15, "input_limit" : 12 },
					),
				},
			),
		},
	),
}
