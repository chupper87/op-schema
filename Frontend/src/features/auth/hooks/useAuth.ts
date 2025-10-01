import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../../../api/client';

export function useAuth() {
    const navigate = useNavigate();

    const loginMutation = useMutation({
        mutationFn: async (credentials: { username: string; password: string }) => {
            const response = await api.post('/auth/login', credentials);
            return response.data;
        },
        onSuccess: (data) => {
            console.log(data);
            localStorage.setItem('token', data.access_token);
            navigate('/');
        },
        onError: (error) => {
            alert("Login Failed");
            console.error(error);
        }
    });
    
    return { 
        login: loginMutation.mutate,
        isLoading: loginMutation.isPending,
        error: loginMutation.error
    };
}