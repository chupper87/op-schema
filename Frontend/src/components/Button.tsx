export default function Button({ onClick }: { onClick?: () => void }) {
    return (
        <button type="submit" 
        onClick={onClick} 
        className="bg-indigo-900 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-800 cursor-pointer">
            Login
            </button>
    );
}