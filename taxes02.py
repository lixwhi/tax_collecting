import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Rectangle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib import rc
from matplotlib.ticker import FormatStrFormatter
np.set_printoptions(precision=15)

rc('font', size=7)
rc('font', family='serif')

rc('axes', labelsize=10)
rc('axes', titlesize='x-large')
rc('axes', edgecolor=(202 / 255, 202 / 255, 202 / 255, 1))
rc('axes', labelpad=26)




rc('grid', color=(242 / 255, 242 / 255, 242 / 255, 242 / 255))
rc('grid', linestyle='-')
rc('grid', linewidth=0.5)

rc('xtick', color=(102 / 255, 102 / 255, 102 / 255, 1))
rc('ytick', color=(102 / 255, 102 / 255, 102 / 255, 1))
rc('xtick', labelsize='large')
rc('ytick', labelsize='large')

rc('figure', figsize= (16, 9))
rc('figure', titlesize='xx-large')
rc('figure', dpi=250)
# liquidation ratio
LR = 1.5
# debt ceiling utilization
DCU = 0.905
# debt ceiling rate offset
DCRO = 0.025
# volatility bias factor
VBF = 2

total_debt = 21200000
fee_target = 1800000
# fix this so that you can show sec at integer multiples of frames instead of sec = frames
num_frames = 61
total_sec = num_frames
min_tax_per_sec   = 0.0000001
max_tax_per_sec   = 0.0003
delta_tax_per_sec = 1000
peth_held_by_borrowers = 390000
min_peth_beneficiaries = 10000
max_peth_beneficiaries = 10000000
delta_peth_beneficiaries = 100
max_z = 10000000
min_z = 0

current_price_of_eth = 230


def tax_curve(x, y, i):
	reb_ratio = get_borrower_reimbursement_ratio(y)

	tax_out = ( x * total_debt * i) / reb_ratio 
	return tax_out
def tax_curve_static(x, i):
	reb_ratio = get_borrower_reimbursement_ratio(x)
	desired_tax_out = fee_target

	y = (desired_tax_out * reb_ratio ) / (total_debt * i)
	
	return y

def get_borrower_reimbursement_ratio(y):
	return peth_held_by_borrowers / (peth_held_by_borrowers + y)

def surface_plot():
	x = np.linspace(min_tax_per_sec, max_tax_per_sec, delta_tax_per_sec)

	# with np.printoptions(threshold=np.inf):
	# 	print(x)
	y = np.linspace(min_peth_beneficiaries, max_peth_beneficiaries, delta_peth_beneficiaries)


	X, Y = np.meshgrid(x, y)

	cmap = plt.get_cmap('twilight_shifted')
	start = 0.42
	stop = 1
	colors = cmap(np.linspace(start, stop, cmap.N))
	color_map = LinearSegmentedColormap.from_list('Upper Half', colors)
	starting_frame = 0

	init_x_view = 35
	final_x_view = 24
	init_y_view = -95
	final_y_view = -111
	x_view = np.linspace(init_x_view, final_x_view, num_frames)
	y_view = np.linspace(init_y_view, final_y_view, num_frames)


	EVEN_STEVEN_COLOR = (113 / 255, 201 / 255, 206 / 255, 55 / 255)


	for i in range(starting_frame, num_frames):
		print(i)
		Z = tax_curve(X, Y, i)
		fig = plt.figure()
		ax = plt.axes(projection='3d')
		
		
		ax.set_title('SCD Shutdown - Tax Parameter Approximation', color=(102 / 255, 102 / 255, 102 / 255, 1), fontsize=15)
		ax.set_zlim([min_z, max_z])
		ax.set_ylim([min_peth_beneficiaries, max_peth_beneficiaries])
		ax.set_xlim(min_tax_per_sec, max_tax_per_sec)
		
		[t.set_va('center') for t in ax.get_yticklabels()]
		[t.set_ha('center') for t in ax.get_yticklabels()]
		[t.set_va('center') for t in ax.get_xticklabels()]
		[t.set_ha('center') for t in ax.get_xticklabels()]
		[t.set_va('center') for t in ax.get_zticklabels()]
		[t.set_ha('center') for t in ax.get_zticklabels()]
		ax.xaxis._axinfo['tick']['inward_factor'] = 0
		ax.xaxis._axinfo['tick']['outward_factor'] = 0.2
		ax.yaxis._axinfo['tick']['inward_factor'] = 0
		ax.yaxis._axinfo['tick']['outward_factor'] = 0.2
		ax.zaxis._axinfo['tick']['inward_factor'] = 0
		ax.zaxis._axinfo['tick']['outward_factor'] = 0.2
		ax.set_xlabel('Tax per second', color=(102 / 255, 102 / 255, 102 / 255, 1))
		ax.set_ylabel('PETH added from non-borrowers (PETH)', color=(102 / 255, 102 / 255, 102 / 255, 1))
		ax.set_zlabel('Tax given to non-borrowing PETH holders (DAI)', color=(102 / 255, 102 / 255, 102 / 255, 1))

		ax.xaxis.set_rotate_label(True)
		ax.yaxis.set_rotate_label(True)
		ax.zaxis.set_rotate_label(True)
		ax.tick_params(axis='both', which='major', pad=15)
		ax.ticklabel_format(axis='both', style='plain')

		ax.text(0, max_peth_beneficiaries * 0.999, fee_target,'target tax = 1.8MM','x', color=(102 / 255, 102 / 255, 102 / 255, 1) )
		ax.text2D(0.15, 0.99, "seconds {0}/{1}".format(i,total_sec - 1), transform=ax.transAxes, color=(102 / 255, 102 / 255, 102 / 255, 1))

		# even_steven = Rectangle((0, 0.001), 0.001, 10000000, color=EVEN_STEVEN_COLOR, zorder=0)
		# ax.add_patch(even_steven)
		# art3d.pathpatch_2d_to_3d(even_steven, z=fee_target, zdir='z')
		# even_steven = Rectangle((0.000005, fee_target), max_tax_per_sec, 100000, color=EVEN_STEVEN_COLOR, zorder=0)
		# ax.add_patch(even_steven)
		# art3d.pathpatch_2d_to_3d(even_steven, z=fee_target, zdir='y')


		surf = ax.plot_surface(X, Y, Z,  cmap=color_map, vmin=min_z, vmax=max_z, edgecolor='none', linewidth=0, antialiased=True, zorder=10)
		
		
		ax.view_init(x_view[i], y_view[i])
		fig.colorbar(surf, ax=ax, shrink=0.8, aspect=8, format='%.0f')
		plt.savefig('out{0}'.format(i), dpi=160)
		fig.clf()
		plt.clf()
		plt.close()

def static_2d_plot():
	

	# with np.printoptions(threshold=np.inf):
	# 	print(x)
	num_seconds_tax = 60
	x = np.linspace(min_peth_beneficiaries, max_peth_beneficiaries, delta_peth_beneficiaries)
	y = tax_curve_static(x, num_seconds_tax)


	EVEN_STEVEN_COLOR = (113 / 255, 201 / 255, 206 / 255, 55 / 255)


	fig = plt.figure()
	ax = fig.add_subplot(111)
	#ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
	ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
	ax.plot(x,y, color=(52 / 255, 52 / 255, 52 / 255, 1))
	
	
	ax.set_title('SCD Shutdown - flash tax before GS - {0} seconds for {1} in stability fees owed'.format(num_seconds_tax, fee_target), color=(102 / 255, 102 / 255, 102 / 255, 1), fontsize=15)
	
	# ax.set_xlim([min_peth_beneficiaries, max_peth_beneficiaries])
	# ax.set_ylim(min_tax_per_sec, max_tax_per_sec)
	

	ax.set_ylabel('Tax per second', color=(102 / 255, 102 / 255, 102 / 255, 1))
	ax.set_xlabel('PETH added from non-borrowers (PETH)', color=(102 / 255, 102 / 255, 102 / 255, 1))
	

	# ax.xaxis.set_rotate_label(True)
	# ax.yaxis.set_rotate_label(True)
	# #ax.zaxis.set_rotate_label(True)
	#ax.tick_params(axis='both', which='major', pad=15)
	#ax.ticklabel_format(axis='both', style='plain')

	#ax.text(0, max_peth_beneficiaries * 0.999, fee_target,'target tax = 1.8MM','x', color=(102 / 255, 102 / 255, 102 / 255, 1) )
	#ax.text2D(0.15, 0.99, "seconds {0}/{1}".format(i,total_sec - 1), transform=ax.transAxes, color=(102 / 255, 102 / 255, 102 / 255, 1))	
	
	
	plt.savefig('outt{0}'.format(2), dpi=160)
	fig.clf()
	plt.clf()
	plt.close()




def main():

	#surface_plot()
	static_2d_plot()
	print("done")


if __name__ == "__main__":
	main()



