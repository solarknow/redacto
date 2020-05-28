class Order:
    def __init__(self, lines):
        """
        Defines schema of data read in.
        :param lines: a List of strings parsed from order PDFs
        """
        self.id = ''
        self.date_placed = ''
        self.order_total = 0
        self.items = []
        self.date_shipped = ''
        self.shipping_loc = {}
        self.shipping_speed = ''
        self.payment_method = ''
        self.billing_loc = {}
        for idx, line in enumerate(lines):
            split_line = line.strip().split(':')
            if split_line[0] == 'Order Placed':
                self.date_placed = split_line[1].strip()
            elif split_line[0] == 'Amazon.com order number':
                self.id = split_line[1].strip()
            elif split_line[0] == 'Order Total':
                self.order_total = float(split_line[1].strip()[1:])
            elif split_line[0].startswith('Shipped on'):
                self.date_shipped = ' '.join(split_line[0].split()[2:])
                stack = lines[idx:]
                for jdx, subline in enumerate(stack):
                    if subline.startswith('Payment Method:'):
                        break
                    elif subline.strip() == 'Price':
                        price = float(stack[jdx + 1].strip().split('$')[1])
                        quantity = int(stack[jdx + 4].split()[0])
                        name = stack[jdx + 4].split(':')[1].strip()
                        sold_by = stack[jdx + 6].split(':')[1].strip()
                        condition = stack[jdx + 8].split(':')[1].strip()
                        self.items.append(OrderItem(name, quantity, price, sold_by, condition))
            elif split_line[0].startswith('Gift Cards'):
                self.date_shipped = self.date_placed
                stack = lines[idx:]
                for jdx, subline in enumerate(stack):
                    if subline.startswith('Payment Method:'):
                        break
                    elif subline.strip() == 'Amount':
                        price = float(stack[jdx + 1].strip().split('$')[1])
                        quantity = 1
                        name = "Gift card"
                        sold_by = "Amazon.com Services LLC"
                        condition = 'New'
                        self.items.append(OrderItem(name, quantity, price, sold_by, condition))
            elif split_line[0] == 'Shipping Address':
                if len(lines[idx + 3].split(',')) == 2:
                    self.shipping_loc = {
                        'City': lines[idx + 3].split(',')[0],
                        'Region': lines[idx + 3].split()[1],
                        'PostalCode': lines[idx + 3].split()[-1].strip(),
                        'Country': lines[idx + 4].strip()
                    }
                else:
                    self.shipping_loc = {
                        'City': lines[idx + 3].split(', ')[0],
                        'Region': lines[idx + 3].split(', ')[1],
                        'PostalCode': lines[idx + 3].split()[-1].strip(),
                        'Country': lines[idx + 3].split(', ')[-1].split()[0]
                    }
            elif split_line[0] == 'Shipping Speed':
                self.shipping_speed = lines[idx + 1].strip()
            elif split_line[0] == 'Payment Method':
                self.payment_method = lines[idx + 1].split()[0]
            elif split_line[0] == 'Billing address':
                if len(lines[idx + 3].split(', ')) == 2:
                    self.billing_loc = {
                        'City': lines[idx + 3].split(', ')[0],
                        'Region': lines[idx + 3].split()[1],
                        'PostalCode': lines[idx + 3].split()[-1].strip(),
                        'Country': lines[idx + 4].strip()
                    }
                else:
                    self.billing_loc = {
                        'City': lines[idx + 3].split(', ')[0],
                        'Region': lines[idx + 3].split(', ')[1],
                        'PostalCode': lines[idx + 3].split()[-1].strip(),
                        'Country': lines[idx + 3].split(', ')[-1].split()[0]
                    }


class OrderItem:
    def __init__(self, name, quantity, price, sold_by, condition):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sold_by = sold_by
        self.condition = condition

    def __eq__(self, other):
        return self.name == other.name and \
               self.quantity == other.quantity and \
               self.price == other.price and \
               self.sold_by == other.sold_by and \
               self.condition == other.condition
