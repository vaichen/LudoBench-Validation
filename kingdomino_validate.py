import json

# Mapping of acceptable terrain synonyms
TERRAIN_SYNONYMS = {
    'water': 'water',
    'lake': 'water',
    'forest': 'forest',
    'woods': 'forest',
    'grassland': 'grassland',
    'field': 'grassland',  # Treat 'field' as 'grassland'
    'wheat': 'wheat',
    'mine': 'mine',
    # Add more synonyms as needed
}

def tileNameNormalization(terrain):
   
    return TERRAIN_SYNONYMS.get(terrain.lower(), terrain.lower())


def extract_squares(kingdom):
    """
    Helper to extract all squares from the PlayersKingdom["dominoes"] list.
    Returns a set of (x, y, normalized_terrain) tuples.
    """
    squares = set()
    for domino in kingdom.get("dominoes", []):
        for tile_squares in domino.values():
            for square in tile_squares:
                norm_terrain = tileNameNormalization(square["terrain"])
                squares.add((square["x"], square["y"], norm_terrain))
    return squares


def evaluate_kingdomino_pred_gamestate(prediction, ground_truth):
    """
    Compares the set of squares in PlayersKingdom between prediction and ground_truth,
    using normalized terrain names and ignoring crowns and tile labels.
    Returns 1 if they match, 0 otherwise.
    """
    gt_kingdom = ground_truth.get("PlayersKingdom", {})
    pred_kingdom = prediction.get("PlayersKingdom", {})
    gt_squares = extract_squares(gt_kingdom)
    pred_squares = extract_squares(pred_kingdom)
    return int(gt_squares == pred_squares)


if __name__ == "__main__":
    with open("ground_truth.json", "r") as f:
        ground_truth = json.load(f)
    with open("test_prediction.json", "r") as f:
        prediction = json.load(f)
    result = evaluate_kingdomino_pred_gamestate(prediction, ground_truth)
    print(f"Evaluation result: {result}")

    # Show differences if not matching
    if not result:
        gt_kingdom = ground_truth.get("PlayersKingdom", {})
        pred_kingdom = prediction.get("PlayersKingdom", {})
        gt_squares = extract_squares(gt_kingdom)
        pred_squares = extract_squares(pred_kingdom)
        missing = gt_squares - pred_squares
        extra = pred_squares - gt_squares
        if missing:
            print("Squares missing from prediction:")
            for sq in sorted(missing):
                print(f"  {sq}")
        if extra:
            print("Squares extra in prediction:")
            for sq in sorted(extra):
                print(f"  {sq}")
        if not missing and not extra:
            print("No differences found, but evaluation failed (possible bug).")
