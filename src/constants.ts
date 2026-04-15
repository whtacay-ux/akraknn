import { Item } from './types';

export const MOCK_ITEMS: Item[] = [
  {
    id: '1',
    name: 'Dolunay Kılıcı +9',
    icon: '⚔️',
    type: 'weapon',
    rarity: 'rare',
    stats: {
      'Saldırı Değeri': 142,
      'Ortalama Zarar': 35,
      'Beceri Hasarı': -12,
    },
    levelRequired: 30,
  },
  {
    id: '2',
    name: 'Siyah Çelik Zırh +9',
    icon: '🛡️',
    type: 'armor',
    rarity: 'epic',
    stats: {
      'Defans': 210,
      'Büyü Dayanıklılığı': 20,
      'Maks. HP': 2000,
    },
    levelRequired: 66,
  },
  {
    id: '3',
    name: 'Kırmızı İksir (B)',
    icon: '🧪',
    type: 'potion',
    rarity: 'common',
    description: '1200 HP yeniler.',
  },
  {
    id: '4',
    name: 'Cennetin Gözü Kolye +9',
    icon: '📿',
    type: 'accessory',
    rarity: 'epic',
    stats: {
      'Büyü Hızı': 20,
      'Delici Vuruş Şansı': 10,
    },
    levelRequired: 54,
  },
  {
    id: '5',
    name: 'Zehir Kılıcı +9',
    icon: '🗡️',
    type: 'weapon',
    rarity: 'legendary',
    stats: {
      'Saldırı Değeri': 237,
      'Ortalama Zarar': 42,
      'Zehirleme Şansı': 8,
    },
    levelRequired: 75,
  },
];
