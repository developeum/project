export class User{
    email: string;
    phone: string;
    first_name: string;
    last_name: {
        id: number;
        name: string;
    };
    city: {
        id: number;
        name: string;
    }
    stack: [{
        id: number;
        name: string;
    }]
}