export default function Button({ 
    text = "Logga in", 
    onClick, 
    disabled, 
    type = "submit" 
}: { 
    text?: string;
    onClick?: () => void;
    disabled?: boolean;
    type?: "submit" | "button";
}) {
    return (
        <button 
            type={type}
            onClick={onClick} 
            className="bg-indigo-900 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 cursor-pointer"
            disabled={disabled}
        >
            {text}
        </button>
    );
}