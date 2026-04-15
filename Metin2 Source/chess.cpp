#include "stdafx.h"
#include "chess.h"
#include "char.h"
#include "packet.h"
#include "desc.h"
#include "char_manager.h"
#include "utils.h"

#ifdef ENABLE_CHESS_SYSTEM

CChessGame::CChessGame(LPCHARACTER pkWhite, LPCHARACTER pkBlack, bool bIsBot)
	: m_pkWhite(pkWhite), m_pkBlack(pkBlack), m_bIsBot(bIsBot), m_bWhiteTurn(true)
{
	InitializeBoard();
}

CChessGame::~CChessGame()
{
}

void CChessGame::InitializeBoard()
{
	memset(m_board, 0, sizeof(m_board));

	// White pieces
	m_board[0][0] = CHESS_PIECE_W_ROOK;
	m_board[0][1] = CHESS_PIECE_W_KNIGHT;
	m_board[0][2] = CHESS_PIECE_W_BISHOP;
	m_board[0][3] = CHESS_PIECE_W_QUEEN;
	m_board[0][4] = CHESS_PIECE_W_KING;
	m_board[0][5] = CHESS_PIECE_W_BISHOP;
	m_board[0][6] = CHESS_PIECE_W_KNIGHT;
	m_board[0][7] = CHESS_PIECE_W_ROOK;
	for (int i = 0; i < 8; ++i) m_board[1][i] = CHESS_PIECE_W_PAWN;

	// Black pieces
	m_board[7][0] = CHESS_PIECE_B_ROOK;
	m_board[7][1] = CHESS_PIECE_B_KNIGHT;
	m_board[7][2] = CHESS_PIECE_B_BISHOP;
	m_board[7][3] = CHESS_PIECE_B_QUEEN;
	m_board[7][4] = CHESS_PIECE_B_KING;
	m_board[7][5] = CHESS_PIECE_B_BISHOP;
	m_board[7][6] = CHESS_PIECE_B_KNIGHT;
	m_board[7][7] = CHESS_PIECE_B_ROOK;
	for (int i = 0; i < 8; ++i) m_board[6][i] = CHESS_PIECE_B_PAWN;
}

bool CChessGame::MakeMove(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y)
{
	bool bWhite = (pkChr == m_pkWhite);
	if (bWhite != m_bWhiteTurn) return false;

	if (!IsValidMove(from_x, from_y, to_x, to_y, bWhite)) return false;

	m_board[to_y][to_x] = m_board[from_y][from_x];
	m_board[from_y][from_x] = CHESS_PIECE_EMPTY;

	m_bWhiteTurn = !m_bWhiteTurn;

	SendMove(m_pkWhite, from_x, from_y, to_x, to_y);
	if (!m_bIsBot && m_pkBlack) SendMove(m_pkBlack, from_x, from_y, to_x, to_y);

	if (m_bIsBot && !m_bWhiteTurn)
	{
		ExecuteBotMove();
	}

	return true;
}

bool CChessGame::IsValidMove(int from_x, int from_y, int to_x, int to_y, bool bWhite)
{
	if (from_x < 0 || from_x > 7 || from_y < 0 || from_y > 7) return false;
	if (to_x < 0 || to_x > 7 || to_y < 0 || to_y > 7) return false;

	BYTE piece = m_board[from_y][from_x];
	if (piece == CHESS_PIECE_EMPTY) return false;

	bool bPieceWhite = (piece >= CHESS_PIECE_W_PAWN && piece <= CHESS_PIECE_W_KING);
	if (bPieceWhite != bWhite) return false;

	// Basic check: can't move to a square occupied by your own piece
	BYTE target = m_board[to_y][to_x];
	if (target != CHESS_PIECE_EMPTY)
	{
		bool bTargetWhite = (target >= CHESS_PIECE_W_PAWN && target <= CHESS_PIECE_W_KING);
		if (bTargetWhite == bWhite) return false;
	}

	// For now, allow all moves that aren't to the same square
	if (from_x == to_x && from_y == to_y) return false;

	int dx = to_x - from_x;
	int dy = to_y - from_y;
	int abs_dx = abs(dx);
	int abs_dy = abs(dy);

	switch (piece)
	{
	case CHESS_PIECE_W_PAWN:
		if (dx == 0)
		{
			if (dy == 1 && target == CHESS_PIECE_EMPTY) return true;
			if (from_y == 1 && dy == 2 && target == CHESS_PIECE_EMPTY && m_board[2][from_x] == CHESS_PIECE_EMPTY) return true;
		}
		else if (abs_dx == 1 && dy == 1 && target != CHESS_PIECE_EMPTY) return true;
		return false;

	case CHESS_PIECE_B_PAWN:
		if (dx == 0)
		{
			if (dy == -1 && target == CHESS_PIECE_EMPTY) return true;
			if (from_y == 6 && dy == -2 && target == CHESS_PIECE_EMPTY && m_board[5][from_x] == CHESS_PIECE_EMPTY) return true;
		}
		else if (abs_dx == 1 && dy == -1 && target != CHESS_PIECE_EMPTY) return true;
		return false;

	case CHESS_PIECE_W_KNIGHT:
	case CHESS_PIECE_B_KNIGHT:
		return (abs_dx == 1 && abs_dy == 2) || (abs_dx == 2 && abs_dy == 1);

	case CHESS_PIECE_W_BISHOP:
	case CHESS_PIECE_B_BISHOP:
		if (abs_dx != abs_dy) return false;
		break; // Check path below

	case CHESS_PIECE_W_ROOK:
	case CHESS_PIECE_B_ROOK:
		if (dx != 0 && dy != 0) return false;
		break; // Check path below

	case CHESS_PIECE_W_QUEEN:
	case CHESS_PIECE_B_QUEEN:
		if (abs_dx != abs_dy && dx != 0 && dy != 0) return false;
		break; // Check path below

	case CHESS_PIECE_W_KING:
	case CHESS_PIECE_B_KING:
		return abs_dx <= 1 && abs_dy <= 1;

	default:
		return false;
	}

	// Path checking for sliding pieces (Bishop, Rook, Queen)
	int step_x = (dx == 0) ? 0 : (dx > 0 ? 1 : -1);
	int step_y = (dy == 0) ? 0 : (dy > 0 ? 1 : -1);
	int cur_x = from_x + step_x;
	int cur_y = from_y + step_y;

	while (cur_x != to_x || cur_y != to_y)
	{
		if (m_board[cur_y][cur_x] != CHESS_PIECE_EMPTY) return false;
		cur_x += step_x;
		cur_y += step_y;
	}

	return true;
}

void CChessGame::ExecuteBotMove()
{
	// Simple random move for the bot
	for (int y = 7; y >= 0; --y)
	{
		for (int x = 0; x < 8; ++x)
		{
			BYTE piece = m_board[y][x];
			if (piece >= CHESS_PIECE_B_PAWN && piece <= CHESS_PIECE_B_KING)
			{
				// Try some random moves
				for (int dy = -1; dy <= 1; ++dy)
				{
					for (int dx = -1; dx <= 1; ++dx)
					{
						int tx = x + dx;
						int ty = y + dy;
						if (IsValidMove(x, y, tx, ty, false))
						{
							m_board[ty][tx] = m_board[y][x];
							m_board[y][x] = CHESS_PIECE_EMPTY;
							m_bWhiteTurn = true;
							SendMove(m_pkWhite, x, y, tx, ty);
							return;
						}
					}
				}
			}
		}
	}
}

void CChessGame::SendGameState(LPCHARACTER pkChr)
{
	if (!pkChr || !pkChr->GetDesc()) return;

	TPacketGCChess pack;
	pack.header = HEADER_GC_CHESS;
	pack.subheader = CHESS_SUBHEADER_GC_START;
	pack.arg1 = m_bIsBot ? 1 : 0;
	pack.arg2 = m_bWhiteTurn ? 1 : 0;
	strlcpy(pack.szName, m_pkBlack ? m_pkBlack->GetName() : "Bot", sizeof(pack.szName));
	pkChr->GetDesc()->Packet(&pack, sizeof(pack));

	// Send board state
	for (int y = 0; y < 8; ++y)
	{
		for (int x = 0; x < 8; ++x)
		{
			if (m_board[y][x] != CHESS_PIECE_EMPTY)
			{
				TPacketGCChess update;
				update.header = HEADER_GC_CHESS;
				update.subheader = CHESS_SUBHEADER_GC_UPDATE;
				update.arg1 = (x << 8) | y;
				update.arg2 = m_board[y][x];
				pkChr->GetDesc()->Packet(&update, sizeof(update));
			}
		}
	}
}

void CChessGame::SendMove(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y)
{
	if (!pkChr || !pkChr->GetDesc()) return;

	TPacketGCChess pack;
	pack.header = HEADER_GC_CHESS;
	pack.subheader = CHESS_SUBHEADER_GC_MOVE;
	pack.arg1 = (from_x << 8) | from_y;
	pack.arg2 = (to_x << 8) | to_y;
	pkChr->GetDesc()->Packet(&pack, sizeof(pack));
}

CChessManager::CChessManager()
{
}

CChessManager::~CChessManager()
{
}

void CChessManager::Invite(LPCHARACTER pkChr, const char* szName)
{
	LPCHARACTER pkTarget = CHARACTER_MANAGER::instance().FindPC(szName);
	if (!pkTarget)
	{
		pkChr->ChatPacket(CHAT_TYPE_INFO, "Target not found.");
		return;
	}

	if (pkTarget == pkChr)
	{
		pkChr->ChatPacket(CHAT_TYPE_INFO, "You cannot invite yourself.");
		return;
	}

	m_mapInvitations[pkChr->GetPlayerID()] = pkTarget->GetPlayerID();

	TPacketGCChess pack;
	pack.header = HEADER_GC_CHESS;
	pack.subheader = CHESS_SUBHEADER_GC_INVITE;
	strlcpy(pack.szName, pkChr->GetName(), sizeof(pack.szName));
	pkTarget->GetDesc()->Packet(&pack, sizeof(pack));

	pkChr->ChatPacket(CHAT_TYPE_INFO, "Invitation sent to %s.", szName);
}

void CChessManager::Accept(LPCHARACTER pkChr, const char* szName)
{
	LPCHARACTER pkInviter = CHARACTER_MANAGER::instance().FindPC(szName);
	if (!pkInviter) return;

	auto it = m_mapInvitations.find(pkInviter->GetPlayerID());
	if (it == m_mapInvitations.end() || it->second != pkChr->GetPlayerID()) return;

	m_mapInvitations.erase(it);

	CChessGame* pkGame = new CChessGame(pkInviter, pkChr);
	m_mapGames[pkInviter->GetPlayerID()] = pkGame;
	m_mapGames[pkChr->GetPlayerID()] = pkGame;

	pkGame->SendGameState(pkInviter);
	pkGame->SendGameState(pkChr);
}

void CChessManager::Decline(LPCHARACTER pkChr, const char* szName)
{
	LPCHARACTER pkInviter = CHARACTER_MANAGER::instance().FindPC(szName);
	if (!pkInviter) return;

	m_mapInvitations.erase(pkInviter->GetPlayerID());
	pkInviter->ChatPacket(CHAT_TYPE_INFO, "%s declined your invitation.", pkChr->GetName());
}

void CChessManager::StartBot(LPCHARACTER pkChr)
{
	CChessGame* pkGame = new CChessGame(pkChr, NULL, true);
	m_mapGames[pkChr->GetPlayerID()] = pkGame;
	pkGame->SendGameState(pkChr);
}

void CChessManager::Move(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y)
{
	auto it = m_mapGames.find(pkChr->GetPlayerID());
	if (it == m_mapGames.end()) return;

	it->second->MakeMove(pkChr, from_x, from_y, to_x, to_y);
}

void CChessManager::Quit(LPCHARACTER pkChr)
{
	auto it = m_mapGames.find(pkChr->GetPlayerID());
	if (it == m_mapGames.end()) return;

	CChessGame* pkGame = it->second;
	LPCHARACTER pkWhite = pkGame->GetWhitePlayer();
	LPCHARACTER pkBlack = pkGame->GetBlackPlayer();

	if (pkWhite) m_mapGames.erase(pkWhite->GetPlayerID());
	if (pkBlack) m_mapGames.erase(pkBlack->GetPlayerID());

	delete pkGame;
}

void CChessManager::OnLogout(LPCHARACTER pkChr)
{
	Quit(pkChr);
	m_mapInvitations.erase(pkChr->GetPlayerID());
}

#endif
