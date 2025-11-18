export default function Button({
  text = 'Logga in',
  onClick,
  disabled,
  type = 'submit',
}: {
  text?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'submit' | 'button';
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      className="cursor-pointer rounded-lg bg-indigo-900 px-4 py-2 font-bold text-white hover:bg-indigo-700"
      disabled={disabled}
    >
      {text}
    </button>
  );
}
