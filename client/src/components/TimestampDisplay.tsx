import { Timestamp } from "@/types/notes";

interface TimestampDisplayProps {
  timestamp: Timestamp;
  className?: string;
}

export default function TimestampDisplay({
  timestamp,
  className = "",
}: TimestampDisplayProps) {
  return (
    <div className={`text-xs text-gray-500 ${className}`}>
      <div className="truncate">
        {new Date(timestamp).toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric",
        })}
      </div>
      <div className="text-gray-400 truncate">
        {new Date(timestamp).toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        })}
      </div>
    </div>
  );
}
