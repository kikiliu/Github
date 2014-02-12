class Node():
	left = None;
	right = None;
	def calc_depth(self):
		left_depth = 0
		if self.left is not None:
			left_depth = self.left.calc_depth()
		right_depth = 0
		if self.right is not None:
			right_depth = self.right.calc_depth()
		return (max(left_depth,right_depth) + 1)
	def calc_diameter(self):
		diameter = 1
		left_diameter = 0
		right_diameter = 0
		if self.left is not None:
			diameter += self.left.calc_depth()
			left_diameter = self.left.calc_diameter()
		if self.right is not None:
			diameter += self.right.calc_depth()
			right_diameter = self.right.calc_diameter()		
		return max(diameter,left_diameter,right_diameter)
if __name__ == '__main__':
	root = Node()
	root.left =Node()
	root.right = Node()
	root.left.left = Node()
	root.left.right = Node()
	root.right.left = Node()
	print root.calc_diameter()
	

