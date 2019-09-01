export function getRoomDisplayName(room) {
  if (room.cardinal) {
    return room.scenario + " - " + room.cardinal
  } else {
    return room.scenario
  }
}