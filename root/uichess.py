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

class ChessWindow(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.SetTitleName("Chess System")
		self.AddFlag("movable")
		self.AddFlag("float")
		self.__LoadWindow()
		self.ResetGame()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

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
		except:
			import exception
			exception.Abort("ChessWindow.__LoadWindow.BindObject")

		self.invite_button.SetEvent(ui.__mem_func__(self.__OnInvite))
		self.bot_button.SetEvent(ui.__mem_func__(self.__OnStartBot))
		self.quit_button.SetEvent(ui.__mem_func__(self.__OnQuit))

		self.pieces = {}
		self.selected_pos = None
		self.is_white = True
		self.is_my_turn = False
		self.opponent_name = ""

		# Create piece images
		for y in range(8):
			for x in range(8):
				slot = ui.SlotWindow()
				slot.SetParent(self.board_grid)
				slot.SetSize(32, 32)
				slot.SetPosition(x * 32, y * 32)
				slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
				slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
				slot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
				slot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
				slot.AppendSlot(0, 0, 0, 32, 32)
				slot.Show()
				self.pieces[(x, y)] = slot

	def ResetGame(self):
		for slot in self.pieces.values():
			slot.ClearSlot(0)
		self.selected_pos = None
		self.is_my_turn = False
		self.status_text.SetText("Ready")

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def __OnInvite(self):
		name = self.name_edit.GetText()
		if not name:
			return
		net.SendChessPacket(CHESS_SUBHEADER_CG_INVITE, name=name)

	def __OnStartBot(self):
		net.SendChessPacket(CHESS_SUBHEADER_CG_START_BOT)

	def __OnQuit(self):
		net.SendChessPacket(CHESS_SUBHEADER_CG_QUIT)
		self.ResetGame()
		self.Close()

	def __OnSelectEmptySlot(self, slotIndex):
		if not self.is_my_turn:
			return
		if self.selected_pos:
			# Move to empty slot
			x, y = self.__GetSlotPos(slotIndex)
			from_x, from_y = self.selected_pos
			net.SendChessPacket(CHESS_SUBHEADER_CG_MOVE, arg1=(from_x << 8) | from_y, arg2=(x << 8) | y)
			self.selected_pos = None

	def __OnSelectItemSlot(self, slotIndex):
		if not self.is_my_turn:
			return
		x, y = self.__GetSlotPos(slotIndex)
		if self.selected_pos:
			# Capture or change selection
			from_x, from_y = self.selected_pos
			net.SendChessPacket(CHESS_SUBHEADER_CG_MOVE, arg1=(from_x << 8) | from_y, arg2=(x << 8) | y)
			self.selected_pos = None
		else:
			self.selected_pos = (x, y)

	def __GetSlotPos(self, slotIndex):
		# This is a bit hacky since we have multiple slot windows
		for pos, slot in self.pieces.items():
			if slot.IsOver():
				return pos
		return (0, 0)

	def __OnOverInItem(self, slotIndex):
		pass

	def __OnOverOutItem(self):
		pass

	def OnInvite(self, name):
		self.opponent_name = name
		self.status_text.SetText("Invitation from %s" % name)
		# Show accept/decline dialog
		import uicommon
		self.questionDialog = uicommon.QuestionDialog()
		self.questionDialog.SetText("%s invites you to Chess. Accept?" % name)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__AcceptInvite))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__DeclineInvite))
		self.questionDialog.Open()

	def __AcceptInvite(self):
		net.SendChessPacket(CHESS_SUBHEADER_CG_ACCEPT, name=self.opponent_name)
		self.questionDialog.Close()
		self.questionDialog = None

	def __DeclineInvite(self):
		net.SendChessPacket(CHESS_SUBHEADER_CG_DECLINE, name=self.opponent_name)
		self.questionDialog.Close()
		self.questionDialog = None

	def OnStart(self, is_bot, is_white, opponent_name):
		self.is_white = is_white
		self.is_my_turn = is_white
		self.opponent_name = opponent_name
		self.status_text.SetText("Game started against %s" % opponent_name)
		self.Open()

	def OnUpdate(self, x, y, piece):
		# Map piece ID to icon
		icon = self.__GetPieceIcon(piece)
		self.pieces[(x, y)].SetItemSlot(0, icon, 1)

	def OnMove(self, from_x, from_y, to_x, to_y):
		# Update board locally
		piece = self.__GetPieceAt(from_x, from_y)
		self.pieces[(from_x, from_y)].ClearSlot(0)
		self.pieces[(to_x, to_y)].SetItemSlot(0, self.__GetPieceIcon(piece), 1)
		self.is_my_turn = not self.is_my_turn
		self.status_text.SetText("Your turn" if self.is_my_turn else "Opponent's turn")

	def __GetPieceAt(self, x, y):
		# In a real implementation, we'd store the board state
		return 0 

	def __GetPieceIcon(self, piece):
		# Placeholder icons
		icons = {
			CHESS_PIECE_W_PAWN: 10,
			CHESS_PIECE_W_KNIGHT: 11,
			CHESS_PIECE_W_BISHOP: 12,
			CHESS_PIECE_W_ROOK: 13,
			CHESS_PIECE_W_QUEEN: 14,
			CHESS_PIECE_W_KING: 15,
			CHESS_PIECE_B_PAWN: 20,
			CHESS_PIECE_B_KNIGHT: 21,
			CHESS_PIECE_B_BISHOP: 22,
			CHESS_PIECE_B_ROOK: 23,
			CHESS_PIECE_B_QUEEN: 24,
			CHESS_PIECE_B_KING: 25,
		}
		return icons.get(piece, 0)
