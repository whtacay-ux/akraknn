import uiScriptLocale

window = {
	"name" : "ChessWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 400,
	"height" : 450,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 400,
			"height" : 450,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 384,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":192, "y":3, "text":"Chess Game", "text_horizontal_align":"center" },
					),
				},

				## Board Grid
				{
					"name" : "board_grid",
					"type" : "window",

					"x" : 72,
					"y" : 40,

					"width" : 256,
					"height" : 256,
				},

				## Controls
				{
					"name" : "control_window",
					"type" : "window",

					"x" : 10,
					"y" : 310,

					"width" : 380,
					"height" : 130,

					"children" :
					(
						{
							"name" : "name_slot",
							"type" : "slotbar",

							"x" : 10,
							"y" : 10,

							"width" : 120,
							"height" : 18,

							"children" :
							(
								{
									"name" : "name_edit",
									"type" : "editline",

									"x" : 3,
									"y" : 3,

									"width" : 114,
									"height" : 15,

									"input_limit" : 12,
								},
							),
						},
						{
							"name" : "invite_button",
							"type" : "button",

							"x" : 140,
							"y" : 10,

							"text" : "Invite",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "bot_button",
							"type" : "button",

							"x" : 230,
							"y" : 10,

							"text" : "Play with Bot",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "quit_button",
							"type" : "button",

							"x" : 320,
							"y" : 10,

							"text" : "Quit",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "status_text",
							"type" : "text",

							"x" : 190,
							"y" : 50,

							"text" : "Ready",
							"text_horizontal_align" : "center",
						},
					),
				},
			),
		},
	),
}
