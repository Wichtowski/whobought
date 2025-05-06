import { User, Group, Expense } from '../interfaces';

const API_BASE = '/api/v1/whobought';

class BaseService {
    protected async request(endpoint: string, method: string, body?: any): Promise<any> {
        const url = `${API_BASE}${endpoint}`;
        const options: RequestInit = {
            method,
            headers: {
                'Content-Type': 'application/json',
                // Add authentication headers if needed
            },
            body: body ? JSON.stringify(body) : undefined,
        };

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Request failed', error);
            throw error;
        }
    }
}

class UserService extends BaseService {
    async createUser(user: Omit<User, 'id'>): Promise<User> {
        return this.request('/user', 'POST', user);
    }

    async getUser(userId: string): Promise<User | null> {
        return this.request(`/user/${userId}`, 'GET');
    }

    async updateUser(userId: string, user: Partial<User>): Promise<User> {
        return this.request(`/user/${userId}`, 'PUT', user);
    }

    async deleteUser(userId: string): Promise<void> {
        await this.request(`/user/${userId}`, 'DELETE');
    }
}

class GroupService extends BaseService {
    async createGroup(group: Omit<Group, 'id'>): Promise<Group> {
        return this.request('/group', 'POST', group);
    }

    async getGroup(groupId: string): Promise<Group | null> {
        return this.request(`/group/${groupId}`, 'GET');
    }

    async updateGroup(groupId: string, group: Partial<Group>): Promise<Group> {
        return this.request(`/group/${groupId}`, 'PUT', group);
    }

    async deleteGroup(groupId: string): Promise<void> {
        await this.request(`/group/${groupId}`, 'DELETE');
    }
}

class ExpenseService extends BaseService {
    async createExpense(expense: Omit<Expense, 'id'>): Promise<Expense> {
        return this.request('/expense', 'POST', expense);
    }

    async getExpense(expenseId: string): Promise<Expense | null> {
        return this.request(`/expense/${expenseId}`, 'GET');
    }

    async updateExpense(expenseId: string, expense: Partial<Expense>): Promise<Expense> {
        return this.request(`/expense/${expenseId}`, 'PUT', expense);
    }

    async deleteExpense(expenseId: string): Promise<void> {
        await this.request(`/expense/${expenseId}`, 'DELETE');
    }
}

export { UserService, GroupService, ExpenseService }; 