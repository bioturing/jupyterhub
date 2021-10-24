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
import NotebookCardList from './NotebookCard';
import {getPublicNotebooks, getWhoAmI} from '../../services/users';
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

const NotebookPanel: React.FunctionComponent = function(props) {
	const [user, setUser] = useState('nobody');
	useEffect(() => {
		getWhoAmI()
			.then(res => {
				setUser(res.name);
			})
	}, [])

	const [publicNotebooks, setPublicNotebooks] = useState([]);
	useEffect(() => {
		let mounted = true;
		if (user !== 'nobody') {
			getPublicNotebooks()
			.then(model => {
				if(mounted) {
				setPublicNotebooks(model);
				}
			})
		}
		return () => mounted = false;
	      }, [user]);
	return (
	<div>
		<PageSection variant={PageSectionVariants.light}>
			<Flex>
				<TextContent>
					<Text component="h1">Your notebooks </Text>
				</TextContent>
				{/* {publicNotebooks.length !== 0 ? (<Button variant="link" icon={<PlusCircleIcon />} component={props => <NavLink {...props} exact={true} to={normalizeRoute("/new-notebook")}/>}>
					New server
				</Button>) : null} */}
			</Flex>
			
		</PageSection>
		<PageSection> 
			{/* TODO: add loading status here */}
			{publicNotebooks.length !== 0 ? 
				<NotebookCardList 
					servers={Object.values(publicNotebooks) }
					user={user}
					/> : <WelcomeNewServer />}
		</PageSection>
	</div>
	
	)
}

export { NotebookPanel };
