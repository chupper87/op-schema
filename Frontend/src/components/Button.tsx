export default function Button({ onClick, disabled }: { onClick?: () => void, disabled?: boolean }) {
    return (
        <button type="submit" 
        onClick={onClick} 
        className="bg-indigo-900 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-800 cursor-pointer"
        disabled={disabled}>
            Login
            </button>
    );
}