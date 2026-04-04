/**
 * ErrorAlert — displays an error message banner.
 */
export default function ErrorAlert({ message, onDismiss }) {
  if (!message) return null;
  return (
    <div className="mb-4 flex items-center justify-between rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-red-700">
      <span>{message}</span>
      {onDismiss && (
        <button onClick={onDismiss} className="ml-4 font-bold hover:text-red-900">&times;</button>
      )}
    </div>
  );
}
