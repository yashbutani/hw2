SELECT COUNT(DISTINCT Category.Category) FROM Category INNER JOIN Bids ON Category.ItemID = Bids.ItemID WHERE Bids.Amount > 100