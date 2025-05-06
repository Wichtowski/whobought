import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, Group, Expense } from '../../interfaces';
import { websocketService } from '../../services/websocket';

interface StoreState {
    user: User | null;
    currentGroup: Group | null;
    setUser: (user: User | null) => void;
    setCurrentGroup: (groupId: string) => void;
    addExpense: (expense: Omit<Expense, 'id'>) => void;
    removeExpense: (expenseId: string) => void;
    clearExpenses: () => void;
    fetchProtectedData: () => Promise<void>;
    initializeWebSocket: () => void;
}

export const useStore = create<StoreState>()(
    persist(
        (set, get) => ({
            user: null,
            currentGroup: null,
            setUser: (user) => set({ user }),
            setCurrentGroup: async (groupId: string) => {
                const { user } = get();
                if (!user) return;

                const group = user.groupsIds.find(id => id === groupId);
                if (group) {
                    const fetchGroupDetails = async (groupId: string): Promise<Group | null> => {
                        // TODO: Implement actual data fetching logic here
                        return null;
                    };

                    const groupDetails = await fetchGroupDetails(group);
                    if (groupDetails) {
                        set({ currentGroup: groupDetails });
                    }
                }
            },
            addExpense: (expense) => {
                const { currentGroup } = get();
                if (!currentGroup) return;

                const newExpense = {
                    ...expense,
                    id: Date.now().toString(),
                };

                set((state) => ({
                    currentGroup: {
                        ...currentGroup,
                        expenses: [...currentGroup.expenses, newExpense],
                    },
                }));

                websocketService.send('EXPENSE_ADDED', newExpense);
            },
            removeExpense: (expenseId) => {
                const { currentGroup } = get();
                if (!currentGroup) return;

                set((state) => ({
                    currentGroup: {
                        ...currentGroup,
                        expenses: currentGroup.expenses.filter(
                            (expense) => expense.id !== expenseId
                        ),
                    },
                }));

                websocketService.send('EXPENSE_DELETED', expenseId);
            },
            clearExpenses: () => {
                const { currentGroup } = get();
                if (!currentGroup) return;

                set((state) => ({
                    currentGroup: {
                        ...currentGroup,
                        expenses: [],
                    },
                }));
            },
            fetchProtectedData: async () => {
                const fetchUserData = async (): Promise<User | null> => {
                    // TODO: Implement actual data fetching logic here
                    return null;
                };

                const userData = await fetchUserData();
                if (userData) {
                    set({ user: userData });

                    if (userData.groupsIds.length > 0) {
                        const fetchGroupDetails = async (groupId: string): Promise<Group | null> => {
                            // TODO: Implement actual data fetching logic here
                            return null;
                        };

                        const firstGroupDetails = await fetchGroupDetails(userData.groupsIds[0]);
                        if (firstGroupDetails) {
                            set({ currentGroup: firstGroupDetails });
                        }
                    }
                }
            },
            initializeWebSocket: () => {
                const { currentGroup } = get();

                websocketService.subscribe('EXPENSE_ADDED', (expense: Expense) => {
                    if (expense.groupId === currentGroup?.id) {
                        set((state) => ({
                            currentGroup: {
                                ...currentGroup,
                                expenses: [...currentGroup.expenses, expense],
                            },
                        }));
                    }
                });

                websocketService.subscribe('EXPENSE_UPDATED', (expense: Expense) => {
                    if (expense.groupId === currentGroup?.id) {
                        set((state) => ({
                            currentGroup: {
                                ...currentGroup,
                                expenses: currentGroup.expenses.map(e =>
                                    e.id === expense.id ? expense : e
                                ),
                            },
                        }));
                    }
                });

                websocketService.subscribe('EXPENSE_DELETED', (expenseId: string) => {
                    if (currentGroup) {
                        set((state) => ({
                            currentGroup: {
                                ...currentGroup,
                                expenses: currentGroup.expenses.filter(
                                    e => e.id !== expenseId
                                ),
                            },
                        }));
                    }
                });

                websocketService.subscribe('GROUP_UPDATED', (group: Group) => {
                    if (group.id === currentGroup?.id) {
                        set({ currentGroup: group });
                    }
                });
            },
        }),
        {
            name: 'whobought-storage',
        }
    )
); 