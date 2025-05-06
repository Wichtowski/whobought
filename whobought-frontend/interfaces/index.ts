
export interface User {
    id: string;
    name: string;
    email: string;
    groupsIds: Group['id'][];
}

export interface Group {
    id: string;
    name: string;
    members: Member[];
    expenses: Expense[];
}

export interface Member {
    name: string;
    email: string;
}

export interface Expense {
    id: string;
    description: string;
    amount: number;
    paidBy: string;
    splitBetween: string[];
    date: string;
    groupId: string;
}

export interface Settlement {
    from: string;
    to: string;
    amount: number;
    groupId: string;
} 