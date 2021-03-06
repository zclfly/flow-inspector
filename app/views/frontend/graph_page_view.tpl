<script type="text/template" id="graph-page-template">
	<div class="container-fixed dark page-graph">
	    <aside id="sidebar" class="well">
	    	<h5>Layout</h5>
	    	<p>
	    		<a class="btn disabled reset help" 
	    			href="javascript:void(0)"
	    			title="Reset & Force Graph" 
	    			data-content="Shuffle and rearrange all nodes on the canvas.">
	    			Reset & Force Graph</a>
	    	</p>
	    	<p>
	    		<a class="btn disabled force help" 
	    			href="javascript:void(0)"
	    			title="Force Graph" 
	    			data-content="Optimize node arrangement on the canvas based on current positions.">
	    			Force Graph</a>
	    	</p>
	    	<p>
	    		<a class="btn disabled hilbert help" 
	    			href="javascript:void(0)"
	    			title="Hilbert Curve" 
	    			data-content="Set positions of all nodes on the canvas with a Hilber curve.">
	    			Hilbert Curve</a>
	    	</p>
		<p>
			<div class="clearfix help"
				title="Charge"
    				data-content="Charge for Force Graphs. Applies at next push to the force button!"
				<label for="charge">Charge</label>
				<input type="text" id="charge"></input>
			</div>
		</p>
		<p>
			<div class="clearfix help"
				title="Gravity"
    				data-content="Gravity for Force Graphs. Applies to the next push to the force button!"
				<label for="charge">Gravity</label>
				<input type="text" id="gravity"></input>
			</div>
		</p>
		<p>
			<div class="clearfix help"
				title="Link Distance"
    				data-content="Desired Link Distance for Force Graphs. Applies to the next push to the force button!"
				<label for="charge">Link Distance</label>
				<input type="text" id="linkdistance"></input>
			</div>
		</p>
		<!--
	    	<h5>Data Mapping</h5>
	    	<form class="form-stacked">
	    		<fieldset>
	    			<div class="clearfix">
	    				<label for="mappingFoobar">Foobar</label>
	    				<select id="mappingFoobar">
	    					<option>none</option>
	    					<option>foobar1</option>
	    					<option>foobar2</option>
	    				</select>
	    			</div>
	    			<div class="clearfix">
	    				<label for="mappingFoobar">Foobar</label>
	    				<select id="mappingFoobar">
	    					<option>none</option>
	    					<option>foobar1</option>
	    					<option>foobar2</option>
	    				</select>
	    			</div>
	    		</fieldset>
	    	</form>
		-->
	    	<h5>Filters</h5>
	    	<form class="form-stacked">
	    	    	<p>
		    		<a class="btn enabled apply-filter help" 
		    			href="javascript:void(0)"
		    			title="Apply Filter" 
		    			data-content="Applies the filters defined in the fields below.">
		    			Apply Filter</a>
		    	</p>

	    		<fieldset>
				
				<div class="help"
					title="Show Others"
					data-content="nodes beyond the filter limit are summarized into a super node called 'others'. This checkbox defines whether others is shown or omitted.">
						<input type="checkbox" id="showOthers">
						<label for="showOthers">Show Others</label>
						</input>
				</div>
	    			<div class="clearfix help"
	    				title="Node limit"
	    				data-content="Limit the number of nodes. Nodes are sorted by the number of flows that belong to them. Then only the first n nodes will be shown individually. The others will be grouped together.">
	    				<label for="filterNodeLimit">Node limit</label>
	    				<select id="filterNodeLimit">
	    					<option value="0">unlimited</option>
	    					<option value="10">10</option>
	    					<option value="15">15</option>
	    					<option value="20">20</option>
	    					<option value="30">30</option>
	    					<option value="40">40</option>
	    					<option value="50">50</option>
	    					<option value="63">63</option>
	    					<option value="100">100</option>
	    					<option value="150">150</option>
	    					<option value="200">200</option>
	    					<option value="255">255</option>
	    					<option value="300">300</option>
	    					<option value="400">400</option>
	    					<option value="500">500</option>
	    					<option value="1000">1000</option>
	    				</select>
	    			</div>
					<div class="clearfix help"
					title="Protocol"
	    				data-content="Filter for protocols. Enter one protocol per line. Supported Protocols: tcp, udp, icmp, other">
						<label for="filterProtocols">Protocol</label>
						<textarea id="filterProtocols" rows="10"></textarea>
						<div class="clearfix">
							<select id="filterProtocolsType">
								<option value="inclusive">include listed protocols</option>
								<option value="exclusive">exclude listed protocols</option>
							</select>
						</div>
					</div>
					<div class="help"
						title="Port filter"
						data-content="Filter flows by port numbers. Enter one port number per line. Ports can be included in the visualization which means only the listed ports will be shown. Or they can be excluded which means only flows that don't contain such a port number are shown.">
						<div class="clearfix">
							<label for="filterPorts">Ports</label>
							<textarea id="filterPorts" rows="10"></textarea>
						</div>
						<div class="clearfix">
							<select id="filterPortsType">
								<option value="inclusive">include only listed ports</option>
								<option value="exclusive">exclude listed ports</option>
							</select>
						</div>
					</div>
					<div class="help"
						title="IP address filter"
						data-content="Filter flows and node lists by IP addresses. Enter one IP address per line (no subnets are allowed at the moment). Addresses can be included in the visualization which means only the listed addresses will be shown. Or they can e excluded which means only flows that don't contain that address are shown.">
						<div class="clearfix">
							<label for="filterIPs">IP Addresses</label>
							<textarea id="filterIPs" rows="10"></textarea>
						</div>
						<div class="clearfix">
							<select id="filterIPsType">
								<option value="inclusive">include only listed IPs</option>
								<option value="exclusive">exclude listed IPs</option>
							</select>
						</div>
	    		</fieldset>
	    	</form>
	    </aside>
	    <div id="content" class="content">
	    	<div class="scroll">
	    		<div class="canvas"></div>
	    	</div>
	    </div>
		<footer id="footbar" class="well">
	    		<ul class="pills timeline-value">
				<li data-value="flows"><a href="javascript:void(0)"># Flows</a></li>
				<li data-value="packetDeltaCount"><a href="javascript:void(0)"># Packets</a></li>
				<li data-value="octetDeltaCount"><a href="javascript:void(0)"># Bytes</a></li>
			</ul>
		</footer>
	</div>
</script>
