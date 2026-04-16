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
		self.ShowStartingPosition()

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
		except:
			import exception
			exception.Abort("ChessWindow.__LoadWindow.BindObject")

		self.title_bar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.invite_button.SetEvent(ui.__mem_func__(self.__OnInvite))
		self.bot_button.SetEvent(ui.__mem_func__(self.__OnStartBot))
		self.quit_button.SetEvent(ui.__mem_func__(self.__OnQuit))

		self.pieces = {}
		self.board_state = {}
		self.selected_pos = None
		self.is_white = True
		self.is_my_turn = False
		self.opponent_name = ""

		self.path = "d:/ymir work/ui/chess/"

		# Create board background
		self.board_bg = ui.ExpandedImageBox()
		self.board_bg.SetParent(self.board_grid)
		full_path_board = self.path + "board.png"
		if app.IsExistFile(full_path_board):
			self.board_bg.LoadImage(full_path_board)
			# Scale to 256x256 regardless of source size
			(w, h) = (self.board_bg.GetWidth(), self.board_bg.GetHeight())
			if w > 0 and h > 0:
				self.board_bg.SetScale(256.0/float(w), 256.0/float(h))
		self.board_bg.Show()

		# Selection highlight
		self.selection_highlight = ui.ExpandedImageBox()
		self.selection_highlight.SetParent(self.board_grid)
		full_path_select = self.path + "selection.png"
		if app.IsExistFile(full_path_select):
			self.selection_highlight.LoadImage(full_path_select)
			(w, h) = (self.selection_highlight.GetWidth(), self.selection_highlight.GetHeight())
			if w > 0 and h > 0:
				self.selection_highlight.SetScale(32.0/float(w), 32.0/float(h))
		self.selection_highlight.Hide()

		# Create piece images
		for y in range(8):
			for x in range(8):
				slot = ui.Window()
				slot.SetParent(self.board_grid)
				slot.SetSize(32, 32)
				slot.SetPosition(x * 32, y * 32)
				
				# We use a button-like behavior for clicking
				btn = ui.Button()
				btn.SetParent(slot)
				btn.SetSize(32, 32)
				btn.SetPosition(0, 0)
				btn.SetEvent(ui.__mem_func__(self.__OnSelectSlot), (x, y))
				btn.Show()
				
				img = ui.ExpandedImageBox()
				img.SetParent(slot)
				img.SetPosition(0, 0)
				img.Hide()
				
				self.pieces[(x, y)] = {"window": slot, "image": img, "button": btn}
				self.board_state[(x, y)] = CHESS_PIECE_EMPTY

	def ResetGame(self):
		for pos in self.pieces:
			self.pieces[pos]["image"].Hide()
			self.board_state[pos] = CHESS_PIECE_EMPTY
		self.selected_pos = None
		self.selection_highlight.Hide()
		self.is_my_turn = False
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
			icon = self.__GetPieceIcon(piece)
			if app.IsExistFile(icon):
				img = self.pieces[(x, y)]["image"]
				img.LoadImage(icon)
				(w, h) = (img.GetWidth(), img.GetHeight())
				if w > 0 and h > 0:
					img.SetScale(32.0/float(w), 32.0/float(h))
				img.Show()
			else:
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
		path = self.path + "pieces/"
		icons = {
			CHESS_PIECE_W_PAWN: "w_pawn.png",
			CHESS_PIECE_W_KNIGHT: "w_knight.png",
			CHESS_PIECE_W_BISHOP: "w_bishop.png",
			CHESS_PIECE_W_ROOK: "w_rook.png",
			CHESS_PIECE_W_QUEEN: "w_queen.png",
			CHESS_PIECE_W_KING: "w_king.png",
			CHESS_PIECE_B_PAWN: "b_pawn.png",
			CHESS_PIECE_B_KNIGHT: "b_knight.png",
			CHESS_PIECE_B_BISHOP: "b_bishop.png",
			CHESS_PIECE_B_ROOK: "b_rook.png",
			CHESS_PIECE_B_QUEEN: "b_queen.png",
			CHESS_PIECE_B_KING: "b_king.png",
		}
		return path + icons.get(piece, "")
