export interface Item {
  id: string;
  name: string;
  icon: string;
  type: 'weapon' | 'armor' | 'accessory' | 'potion' | 'material';
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  stats?: {
    [key: string]: number;
  };
  description?: string;
  levelRequired?: number;
}

export interface CharacterStats {
  level: number;
  exp: number;
  maxExp: number;
  hp: number;
  maxHp: number;
  sp: number;
  maxSp: number;
  vit: number;
  int: number;
  str: number;
  dex: number;
  statPoints: number;
}

export interface InventorySlot {
  id: number;
  item: Item | null;
}
