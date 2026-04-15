#ifndef __INC_METIN2_GAME_CHESS_H__
#define __INC_METIN2_GAME_CHESS_H__

#include "stdafx.h"

#ifdef ENABLE_CHESS_SYSTEM

enum EChessPiece
{
	CHESS_PIECE_EMPTY = 0,
	CHESS_PIECE_W_PAWN,
	CHESS_PIECE_W_KNIGHT,
	CHESS_PIECE_W_BISHOP,
	CHESS_PIECE_W_ROOK,
	CHESS_PIECE_W_QUEEN,
	CHESS_PIECE_W_KING,
	CHESS_PIECE_B_PAWN,
	CHESS_PIECE_B_KNIGHT,
	CHESS_PIECE_B_BISHOP,
	CHESS_PIECE_B_ROOK,
	CHESS_PIECE_B_QUEEN,
	CHESS_PIECE_B_KING,
};

class CChessGame
{
public:
	CChessGame(LPCHARACTER pkWhite, LPCHARACTER pkBlack, bool bIsBot = false);
	~CChessGame();

	bool IsWhiteTurn() const { return m_bWhiteTurn; }
	bool IsBotGame() const { return m_bIsBot; }

	LPCHARACTER GetWhitePlayer() const { return m_pkWhite; }
	LPCHARACTER GetBlackPlayer() const { return m_pkBlack; }

	bool MakeMove(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y);
	void EndGame(LPCHARACTER pkWinner);

	void SendGameState(LPCHARACTER pkChr);
	void SendMove(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y);

private:
	void InitializeBoard();
	bool IsValidMove(int from_x, int from_y, int to_x, int to_y, bool bWhite);
	void ExecuteBotMove();

	LPCHARACTER m_pkWhite;
	LPCHARACTER m_pkBlack;
	bool m_bIsBot;
	bool m_bWhiteTurn;
	BYTE m_board[8][8];
};

class CChessManager : public singleton<CChessManager>
{
public:
	CChessManager();
	virtual ~CChessManager();

	void Invite(LPCHARACTER pkChr, const char* szName);
	void Accept(LPCHARACTER pkChr, const char* szName);
	void Decline(LPCHARACTER pkChr, const char* szName);
	void StartBot(LPCHARACTER pkChr);
	
	void Move(LPCHARACTER pkChr, int from_x, int from_y, int to_x, int to_y);
	void Quit(LPCHARACTER pkChr);

	void OnLogout(LPCHARACTER pkChr);

private:
	std::map<DWORD, CChessGame*> m_mapGames;
	std::map<DWORD, DWORD> m_mapInvitations; // Inviter PID -> Invited PID
};

#endif

#endif
