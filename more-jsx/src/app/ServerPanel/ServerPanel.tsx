import React, { useEffect, useState } from 'react';

import { 
	PageSection, 
	Flex,
	Text,
	TextContent,
  	PageSectionVariants,
	Button,
	FlexItem
} from '@patternfly/react-core';
import PlusCircleIcon from '@patternfly/react-icons/dist/esm/icons/plus-circle-icon';
import ArrowRightIcon from '@patternfly/react-icons/dist/esm/icons/arrow-right-icon';
import ServerCardList from './ServerCard';
import {getWhoAmI} from '../../services/users';
import { NavLink } from 'react-router-dom';
import {normalizeRoute} from '../routes';


const WelcomeNewServer: React.FunctionComponent = function(props) {
	return (
		<Flex alignItems={{default: 'alignItemsCenter'}} direction={{default: 'column'}} justifyContent={{ default: 'justifyContentSpaceBetween' }}>
			<FlexItem>
				<Text>
					You don't have any notebook server yet.
				</Text>
			</FlexItem>
			<FlexItem>
				<Button variant="primary" isLarge component={props => <NavLink {...props} exact={true} to={normalizeRoute("/new-notebook")}/>}>
					Create a notebook server <ArrowRightIcon />
				</Button>
			</FlexItem>
		</Flex>
	
	)
}

const ServerPanel: React.FunctionComponent = function(props) {
	const [userModel, setuserModel] = useState({profile_list:[]});
	const [userServers, setUserServers] = useState({});
	useEffect(() => {
		let mounted = true;
		getWhoAmI()
		  .then(model => {
		    if(mounted) {
		      setuserModel(model);
					setUserServers(model.servers);
		    }
		  })
		return () => mounted = false;
	      }, [])
	return (
	<div>
		<PageSection variant={PageSectionVariants.light}>
			<Flex>
				<TextContent>
					<Text component="h1">Your notebook servers</Text>
				</TextContent>
				{Object.keys(userServers).length !== 0 ? (<Button variant="link" icon={<PlusCircleIcon />} component={props => <NavLink {...props} exact={true} to={normalizeRoute("/new-notebook")}/>}>
					New server
				</Button>) : null}
			</Flex>
			
		</PageSection>
		<PageSection> 
			{/* TODO: add loading status here */}
			{Object.keys(userServers).length !== 0 ? 
				<ServerCardList 
					servers={Object.values(userServers) }
					profileList={userModel.profile_list}
					/> : <WelcomeNewServer />}
		</PageSection>
	</div>
	
	)
}

export { ServerPanel };
