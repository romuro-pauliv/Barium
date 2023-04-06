from string import digits

def amount_validation(value: str, mode: str) -> bool | str:
    new_value: str = ""
    add_characters: str = ".,-"
    char_status: dict[str, dict[str, int]] = {
        "amount": {"dot": 0, "bar": 0, "number": 0},
        "max_amount": {"dot": 1, "bar": 1, "number": 17},
        "min_amount": {"dot": 0, "bar": 0, "number": 1}
    }
    for char_ in value:
        if char_ not in str(digits + add_characters):
            return False
        
        if char_ in digits:
            char_status["amount"]["number"] += 1
            if char_status["amount"]["number"] > char_status["max_amount"]["number"]:
                return False
            new_value += char_
        
        if char_ in ".,":
            char_status["amount"]["dot"] += 1
            if char_status["amount"]["dot"] > char_status["max_amount"]["dot"]:
                return False
            new_value += "."
        
        if char_ == "-":
            char_status["amount"]["bar"] += 1
            if char_status["amount"]["bar"] > char_status["max_amount"]["bar"]:
                return False
            new_value += "-"
    
    for keys in char_status["amount"].keys():
        if char_status["amount"][keys] < char_status["min_amount"][keys]:
            return False
    
    if char_status["amount"]["bar"] != 0 and new_value[0] != "-":
        return False
    
    if char_status["amount"]["dot"] != 0:
      terms: list[str] = new_value.split(".")
      if len(terms[1]) > 2:
          return False
    
    return True if mode == "validation" else float(new_value)