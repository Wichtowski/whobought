import { User, Group, Expense } from '../interfaces';

class WebSocketService {
    private ws: WebSocket | null = null;
    private subscribers: Map<string, Set<(data: any) => void>> = new Map();

    constructor() {
        this.connect();
    }

    private connect() {
        // TODO: Implement proper WebSocket connection
        // this.ws = new WebSocket('ws://your-websocket-server');
        // this.ws.onmessage = this.handleMessage.bind(this);
        // this.ws.onclose = () => setTimeout(() => this.connect(), 1000);
    }

    private handleMessage(event: MessageEvent) {
        try {
            const data = JSON.parse(event.data);
            const subscribers = this.subscribers.get(data.type);
            if (subscribers) {
                subscribers.forEach(callback => callback(data.payload));
            }
        } catch (error) {
            console.error('Error handling WebSocket message:', error);
        }
    }

    public subscribe(event: string, callback: (data: any) => void) {
        if (!this.subscribers.has(event)) {
            this.subscribers.set(event, new Set());
        }
        this.subscribers.get(event)?.add(callback);
    }

    public unsubscribe(event: string, callback: (data: any) => void) {
        this.subscribers.get(event)?.delete(callback);
    }

    public send(event: string, data: any) {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type: event, payload: data }));
        }
    }
}

export const websocketService = new WebSocketService(); 