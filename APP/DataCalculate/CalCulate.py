def CalPurchaseCost(purchase_dict):
    other_expenses = float(purchase_dict['newPurchaseFreight']) + float(purchase_dict['newPurchaseOther'])
    total_number = 0
    new_atom_dict = {}
    for purchase in purchase_dict["purchaseList"]:
        name = "prid" + str(purchase["atomId"])
        number = int(purchase["number"])
        cost = float(purchase["unitPrice"])
        if name in new_atom_dict.keys():
            new_atom_dict[name]["quantity"] += number
            new_atom_dict[name]["cost"] = round(
                (cost * number + new_atom_dict[name]["cost"] * new_atom_dict[name]["quantity"])
                / (number + new_atom_dict[name]["quantity"]), 2)
        else:
            new_atom_dict[name] = {
                'id': purchase["atomId"],
                'quantity': number,
                "cost": cost
            }
        total_number += float(purchase["number"])

    increase_price_add = round(other_expenses / total_number, 2)
    for key, values in new_atom_dict.items():
        values['cost'] = "{:.2f}".format(float(values['cost']) + increase_price_add)
    return new_atom_dict


def CalAtomCost(new_purchase_dict, now_atom_dict):
    refresh_purchase_list = []
    for key in new_purchase_dict.keys():
        total_quantity = float(new_purchase_dict[key]['quantity']) + float(now_atom_dict[key]['quantity'])
        total_cost = float(new_purchase_dict[key]['quantity']) * float(new_purchase_dict[key]['cost']) + float(
            now_atom_dict[key]['quantity']) * float(now_atom_dict[key]['cost'])
        refresh_unit_price = "{:.2f}".format(total_cost / total_quantity)
        refresh_dict = {
            "id": new_purchase_dict[key]["id"],
            "quantity": total_quantity,
            "cost": refresh_unit_price,
        }
        refresh_purchase_list.append(refresh_dict)
        print(refresh_purchase_list)
    return refresh_purchase_list


def AccountBasicData(profile_data):
    if not profile_data['fans']:
        profile_data['fans'] = 1
    if profile_data['liked'] and profile_data['fans']:
        profile_data['liked_rate'] = round(float(profile_data['liked']) / float(profile_data['fans']), 2)
    if profile_data['collected'] and profile_data['fans']:
        profile_data['collected_rate'] = round(float(profile_data['collected']) / float(profile_data['fans']), 2)
    else:
        profile_data['liked_rate'] = 0
        profile_data['collected_rate'] = 0
    if profile_data['liked'] and profile_data['notes']:
        profile_data['ave_liked'] = round(float(profile_data['liked']) / float(profile_data['notes']), 2)
    if profile_data['collected'] and profile_data['notes']:
        profile_data['ave_collected'] = round(float(profile_data['collected']) / float(profile_data['notes']), 2)
    else:
        profile_data['ave_liked'] = 0
        profile_data['ave_collected'] = 0
    return profile_data
