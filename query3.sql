SELECT COUNT(*) as num_auctions_with_4_categories
FROM (
    SELECT i.ItemID, COUNT(DISTINCT c.Category) as num_categories
    FROM Item i
    JOIN Category c ON i.ItemID = c.ItemID
    GROUP BY i.ItemID
    HAVING num_categories = 4
) as temp;