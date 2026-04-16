import ui
import net
import chat
import localeInfo
import constInfo
import app

CHESS_PIECE_EMPTY = 0
CHESS_PIECE_W_PAWN = 1
CHESS_PIECE_W_KNIGHT = 2
CHESS_PIECE_W_BISHOP = 3
CHESS_PIECE_W_ROOK = 4
CHESS_PIECE_W_QUEEN = 5
CHESS_PIECE_W_KING = 6
CHESS_PIECE_B_PAWN = 7
CHESS_PIECE_B_KNIGHT = 8
CHESS_PIECE_B_BISHOP = 9
CHESS_PIECE_B_ROOK = 10
CHESS_PIECE_B_QUEEN = 11
CHESS_PIECE_B_KING = 12

CHESS_SUBHEADER_CG_INVITE = 0
CHESS_SUBHEADER_CG_ACCEPT = 1
CHESS_SUBHEADER_CG_DECLINE = 2
CHESS_SUBHEADER_CG_MOVE = 3
CHESS_SUBHEADER_CG_QUIT = 4
CHESS_SUBHEADER_CG_START_BOT = 5

CHESS_SUBHEADER_GC_INVITE = 0
CHESS_SUBHEADER_GC_START = 1
CHESS_SUBHEADER_GC_MOVE = 2
CHESS_SUBHEADER_GC_END = 3
CHESS_SUBHEADER_GC_UPDATE = 4

class ChessWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.ResetGame()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/chesswindow.py")
		except:
			import exception
			exception.Abort("ChessWindow.__LoadWindow.LoadObject")

		try:
			self.board_grid = self.GetChild("board_grid")
			self.invite_button = self.GetChild("invite_button")
			self.bot_button = self.GetChild("bot_button")
			self.quit_button = self.GetChild("quit_button")
			self.name_edit = self.GetChild("name_edit")
			self.status_text = self.GetChild("status_text")
			self.title_bar = self.GetChild("TitleBar")

			# Yeni nesneler
			self.history_panel = self.GetChild("history_panel")
			self.clock_panel = self.GetChild("clock_panel")
			self.black_time = self.GetChild("BlackTime")
			self.white_time = self.GetChild("WhiteTime")
			self.main_bg = self.GetChild("MainBackground")
			self.close_button = self.GetChild("CloseButton")
		except:
			import exception
			exception.Abort("ChessWindow.__LoadWindow.BindObject")

		self.close_button.SetEvent(ui.__mem_func__(self.Close))
		self.invite_button.SetEvent(ui.__mem_func__(self.__OnInvite))
		self.bot_button.SetEvent(ui.__mem_func__(self.__OnStartBot))
		self.quit_button.SetEvent(ui.__mem_func__(self.__OnQuit))

		self.pieces = {}
		self.board_state = {}
		self.selected_pos = None
		self.is_white = True
		self.is_my_turn = False
		self.opponent_name = ""

		# Path options for robustness
		self.path_list = [
			"d:/ymir work/ui/chess/",
			"ymir work/ui/chess/",
			"ui/chess/",
		]
		self.path = self.path_list[0] # Default

		# Create a container that is NOT scaled to hold the board and pieces
		# Yeni tasarimda tahta 320x320 (8x40)
		self.board_container = ui.Window()
		self.board_container.SetParent(self.board_grid)
		self.board_container.SetPosition(0, 0)
		self.board_container.SetSize(320, 320)
		self.board_container.Show()

		# Create board background
		self.board_bg = ui.ExpandedImageBox()
		self.board_bg.SetParent(self.board_container)
		self.board_bg.AddFlag("not_pick")
		full_path_board = self.path + "board.tga"
		if app.IsExistFile(full_path_board):
			self.board_bg.LoadImage(full_path_board)
			(w, h) = (self.board_bg.GetWidth(), self.board_bg.GetHeight())
			if w > 0 and h > 0:
				self.board_bg.SetScale(320.0/float(w), 320.0/float(h))
		self.board_bg.Show()

		# Arkaplan panellerini güvenli yükle (Crash koruması)
		self.__SafeLoadBackground(self.history_panel, "panel_history.tga")
		self.__SafeLoadBackground(self.clock_panel, "panel_clock.tga")

		# Selection highlight
		self.selection_highlight = ui.ExpandedImageBox()
		self.selection_highlight.SetParent(self.board_container)

		# Arkaplan resmi olceklendirme (640x480 sığdır)
		if self.main_bg:
			(w, h) = (self.main_bg.GetWidth(), self.main_bg.GetHeight())
			if w > 0 and h > 0:
				self.main_bg.SetScale(640.0/float(w), 480.0/float(h))
		self.selection_highlight.AddFlag("not_pick")
		
		# Proaktif kontrol: selection.png/tga nerede?
		path_options = [
			self.path + "selection.tga", self.path + "selection.png", 
			self.path + "pieces/selection.tga", self.path + "pieces/selection.png"
		]
		found_select = False
		for p in path_options:
			if app.IsExistFile(p):
				self.selection_highlight.LoadImage(p)
				found_select = True
				break
		
		if found_select:
			(w, h) = (self.selection_highlight.GetWidth(), self.selection_highlight.GetHeight())
			if w > 0 and h > 0:
				# 40x40 kareler icin
				self.selection_highlight.SetScale(40.0/float(w), 40.0/float(h))
		self.selection_highlight.Hide()

		# Create piece images
		for y in range(8):
			for x in range(8):
				slot = ui.Window()
				slot.SetParent(self.board_container)
				slot.SetPosition(x * 40, y * 40)
				slot.SetSize(40, 40)
				slot.Show()
				
				# Tıklama butonu
				btn = ui.Button()
				btn.SetParent(slot)
				btn.SetPosition(0, 0)
				btn.SetSize(40, 40)
				btn.SetEvent(ui.__mem_func__(self.__OnSelectSlot), (x, y))
				btn.Show()
				
				# Taş resmi - 40x40 icinde 34x34 boyutuyla tam merkezleme (3, 3)
				img = ui.ExpandedImageBox()
				img.SetParent(slot)
				img.SetPosition(3, 3) 
				img.Hide()
				
				self.pieces[(x, y)] = {"window": slot, "image": img, "button": btn}
				self.board_state[(x, y)] = CHESS_PIECE_EMPTY

	def __SafeLoadBackground(self, parent, filename):
		full_path = self.path + filename
		if app.IsExistFile(full_path):
			img = ui.ImageBox()
			img.SetParent(parent)
			img.LoadImage(full_path)
			img.Show()
			if not hasattr(self, "background_images"):
				self.background_images = []
			self.background_images.append(img)
		else:
			import chat
			chat.AppendChat(1, "Eksik Panel Resmi: " + full_path)

	def ResetGame(self):
		for pos in self.pieces:
			self.pieces[pos]["image"].Hide()
			self.board_state[pos] = CHESS_PIECE_EMPTY
		self.selected_pos = None
		self.selection_highlight.Hide()
		self.is_my_turn = False
		self.opponent_name = ""
		self.status_text.SetText("Beklemede")

	def ShowStartingPosition(self):
		self.ResetGame()
		# White pieces (Bottom)
		for x in range(8): self.OnUpdateBoard(x, 6, CHESS_PIECE_W_PAWN)
		self.OnUpdateBoard(0, 7, CHESS_PIECE_W_ROOK); self.OnUpdateBoard(7, 7, CHESS_PIECE_W_ROOK)
		self.OnUpdateBoard(1, 7, CHESS_PIECE_W_KNIGHT); self.OnUpdateBoard(6, 7, CHESS_PIECE_W_KNIGHT)
		self.OnUpdateBoard(2, 7, CHESS_PIECE_W_BISHOP); self.OnUpdateBoard(5, 7, CHESS_PIECE_W_BISHOP)
		self.OnUpdateBoard(3, 7, CHESS_PIECE_W_QUEEN); self.OnUpdateBoard(4, 7, CHESS_PIECE_W_KING)

		# Black pieces (Top)
		for x in range(8): self.OnUpdateBoard(x, 1, CHESS_PIECE_B_PAWN)
		self.OnUpdateBoard(0, 0, CHESS_PIECE_B_ROOK); self.OnUpdateBoard(7, 0, CHESS_PIECE_B_ROOK)
		self.OnUpdateBoard(1, 0, CHESS_PIECE_B_KNIGHT); self.OnUpdateBoard(6, 0, CHESS_PIECE_B_KNIGHT)
		self.OnUpdateBoard(2, 0, CHESS_PIECE_B_BISHOP); self.OnUpdateBoard(5, 0, CHESS_PIECE_B_BISHOP)
		self.OnUpdateBoard(3, 0, CHESS_PIECE_B_QUEEN); self.OnUpdateBoard(4, 0, CHESS_PIECE_B_KING)

	def Open(self):
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		self.Hide()

	def __OnInvite(self):
		name = self.name_edit.GetText()
		if not name:
			return
		if hasattr(net, "SendChessPacket"):
			net.SendChessPacket(CHESS_SUBHEADER_CG_INVITE, name)
		else:
			chat.AppendChat(1, "HATA: Client Source derlenmemis! net.SendChessPacket bulunamadi.")

	def __OnStartBot(self):
		if hasattr(net, "SendChessPacket"):
			net.SendChessPacket(CHESS_SUBHEADER_CG_START_BOT)
		else:
			chat.AppendChat(1, "HATA: Client Source derlenmemis!")

	def __OnQuit(self):
		if hasattr(net, "SendChessPacket"):
			net.SendChessPacket(CHESS_SUBHEADER_CG_QUIT)
		self.ResetGame()
		self.Close()

	def __OnSelectSlot(self, pos):
		if not self.is_my_turn:
			return
		
		x, y = pos
		piece = self.board_state[pos]
		
		if self.selected_pos:
			from_x, from_y = self.selected_pos
			if from_x == x and from_y == y:
				self.selected_pos = None
				self.selection_highlight.Hide()
				return
			
			if hasattr(net, "SendChessPacket"):
				net.SendChessPacket(CHESS_SUBHEADER_CG_MOVE, "", (from_x << 8) | from_y, (x << 8) | y)
			self.selected_pos = None
			self.selection_highlight.Hide()
		else:
			if piece != CHESS_PIECE_EMPTY:
				# Check if it's our piece
				is_piece_white = (piece >= CHESS_PIECE_W_PAWN and piece <= CHESS_PIECE_W_KING)
				if is_piece_white == self.is_white:
					self.selected_pos = (x, y)
					self.selection_highlight.SetPosition(x * 32, y * 32)
					self.selection_highlight.Show()

	def OnInvite(self, name):
		self.opponent_name = name
		self.status_text.SetText("%s Davet Gönderdi" % name)
		# Show accept/decline dialog
		import uiCommon
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText("%s seninle satranc oynamak istiyor. Kabul ediyor musun?\n(Siyah taslarla oynayacaksin)" % name)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__AcceptInvite))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__DeclineInvite))
		self.questionDialog.Open()

	def __AcceptInvite(self):
		if hasattr(net, "SendChessPacket"):
			net.SendChessPacket(CHESS_SUBHEADER_CG_ACCEPT, self.opponent_name)
		self.questionDialog.Close()
		self.questionDialog = None

	def __DeclineInvite(self):
		if hasattr(net, "SendChessPacket"):
			net.SendChessPacket(CHESS_SUBHEADER_CG_DECLINE, self.opponent_name)
		self.questionDialog.Close()
		self.questionDialog = None

	def OnStart(self, is_bot, is_white, opponent_name):
		self.ResetGame() # Clears visual position before game sync
		self.is_white = is_white
		self.is_my_turn = is_white
		self.opponent_name = opponent_name
		
		color_text = "(Beyaz)" if is_white else "(Siyah)"
		self.status_text.SetText("Rakip: %s %s" % (opponent_name, color_text))
		self.Open()

	def OnUpdateBoard(self, x, y, piece):
		self.board_state[(x, y)] = piece
		if piece == CHESS_PIECE_EMPTY:
			self.pieces[(x, y)]["image"].Hide()
		else:
			base_icon_name = self.__GetPieceIcon(piece)
			final_path = ""
			
			# Try all path options
			for base_path in self.path_list:
				# Prioritize .tga, then .png, then no extension
				extensions = [".tga", ".png", ""]
				found = False
				for ext in extensions:
					test_path = base_path + "pieces/" + base_icon_name + ext
					if app.IsExistFile(test_path):
						final_path = test_path
						found = True
						break
				if found:
					break
			
			if final_path:
				img = self.pieces[(x, y)]["image"]
				img.LoadImage(final_path)
				(w, h) = (img.GetWidth(), img.GetHeight())
				if w > 0 and h > 0:
					# 28x28 boyutuna getirip 32x32 icinde ortaliyoruz
					img.SetScale(28.0/float(w), 28.0/float(h))
				img.Show()
			else:
				# Hala bulunamazsa debug icin chat'e yaz
				import chat
				chat.AppendChat(1, "Eksik Resim: " + str(base_icon_name))
				self.pieces[(x, y)]["image"].Hide()

	def OnUpdate(self):
		pass

	def OnMove(self, from_x, from_y, to_x, to_y):
		piece = self.board_state[(from_x, from_y)]
		self.OnUpdateBoard(from_x, from_y, CHESS_PIECE_EMPTY)
		self.OnUpdateBoard(to_x, to_y, piece)
		
		self.is_my_turn = not self.is_my_turn
		self.status_text.SetText("Sıra Sende" if self.is_my_turn else "Rakip Oynuyor")

	def __GetPieceIcon(self, piece):
		icons = {
			CHESS_PIECE_W_PAWN: "w_pawn",
			CHESS_PIECE_W_KNIGHT: "w_knight",
			CHESS_PIECE_W_BISHOP: "w_bishop",
			CHESS_PIECE_W_ROOK: "w_rook",
			CHESS_PIECE_W_QUEEN: "w_queen",
			CHESS_PIECE_W_KING: "w_king",
			CHESS_PIECE_B_PAWN: "b_pawn",
			CHESS_PIECE_B_KNIGHT: "b_knight",
			CHESS_PIECE_B_BISHOP: "b_bishop",
			CHESS_PIECE_B_ROOK: "b_rook",
			CHESS_PIECE_B_QUEEN: "b_queen",
			CHESS_PIECE_B_KING: "b_king",
		}
		return icons.get(piece, "")
