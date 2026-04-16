import uiScriptLocale

window = {
	"name" : "ChessWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 320,
	"height" : 420,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 320,
			"height" : 420,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 304,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":152, "y":3, "text":"Satranc Sistemi", "text_horizontal_align":"center" },
					),
				},

				## Board Grid
				{
					"name" : "board_grid",
					"type" : "window",

					"x" : 32,
					"y" : 40,

					"width" : 256,
					"height" : 256,
				},

				## Controls
				{
					"name" : "control_window",
					"type" : "window",

					"x" : 10,
					"y" : 305,

					"width" : 304,
					"height" : 110,

					"children" :
					(
						{
							"name" : "name_slot",
							"type" : "slotbar",

							"x" : 0,
							"y" : 5,

							"width" : 100,
							"height" : 18,

							"children" :
							(
								{
									"name" : "name_edit",
									"type" : "editline",

									"x" : 3,
									"y" : 3,

									"width" : 94,
									"height" : 15,

									"input_limit" : 12,
								},
							),
						},
						{
							"name" : "invite_button",
							"type" : "button",

							"x" : 105,
							"y" : 4,

							"text" : "Davet Et",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "bot_button",
							"type" : "button",

							"x" : 195,
							"y" : 4,

							"text" : "Botla Oyna",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "status_text",
							"type" : "text",

							"x" : 152,
							"y" : 35,

							"text" : "Oyun Hazir",
							"text_horizontal_align" : "center",
						},
						{
							"name" : "quit_button",
							"type" : "button",

							"x" : 77,
							"y" : 60,

							"text" : "Oyundan Ayril / Pes Et",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
						},
					),
				},
			),
		},
	),
}
