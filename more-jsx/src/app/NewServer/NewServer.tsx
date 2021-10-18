import React, { useEffect, useState } from 'react';
import { Redirect } from 'react-router';

import { 
	PageSection, 
	Text,
	TextContent,
  	PageSectionVariants,
	Button,
	Radio,
	Form, FormGroup, TextInput,
	Grid, GridItem, Flex
} from '@patternfly/react-core';
import PropTypes from 'prop-types';
import { getWhoAmI } from '../../services/users';
import { spawnNewserver } from '../../services/server';
import {normalizeRoute} from '../routes';
import { css } from '@patternfly/react-styles';
import './style.css'

const ServerProfileRadio: React.FunctionComponent = function(props) {
	const {
		profileList,
		updateProfileCallback
	} = props;
	const [checkState, setCheckState] = useState({});

	const initState = {};
	for (let i = 0 ; i < profileList.length; ++i) {
		initState[`profile-check-${i}`] = false;
	}
      
	const handleChange = function(_, event) {
	    const { value } = event.currentTarget;
	    const updateCheckStatus = function(prevState) {
		for (let s in prevState) {
			prevState[s] = false;
		}
		return {...prevState, [value]: true}
	    }
	    setCheckState(updateCheckStatus);
	    updateProfileCallback(event.target.name);
	};
	const renderLabel = function(profile) {
		const spec = profile["kubespawner_override"];
		return `Docker image: ${spec["image"]} - CPU(s): ${spec["cpu_limit"]} - RAM: ${spec["mem_limit"]}`
	}
	const renderOneRadio = function(profile, index) {
		const checkStr = `profile-check-${index}`;
		return (
			<Radio
				isChecked={checkState[checkStr]}
				name={profile.slug}
				onChange={handleChange}
				description={renderLabel(profile)}
				label={profile.display_name}	
				id={`profile-radio-${index}`}
				value={checkStr}
	      		/>
		)	
	}

	  return (
	    <React.Fragment>
		{profileList.map((profile, index) => renderOneRadio(profile, index))}
	    </React.Fragment>
	  );
}

const ButtonProgressVariants = (props) => {
	const {
		onClickFunc,
		spawningStatus,
		isDisabled
	} = props;
	const [isPrimaryLoading, setIsPrimaryLoading] = React.useState(false);
	const extraPrimaryProps = {};
	if (isPrimaryLoading) {
	  extraPrimaryProps.spinnerAriaValueText = 'Loading';
	}

	const handleClick = function() {
		setIsPrimaryLoading(true);
		onClickFunc(setIsPrimaryLoading);
	}
	return (
	  <React.Fragment>
	    <Button
	      spinnerAriaValueText={isPrimaryLoading ? 'Loading' : undefined}
	      isLoading={isPrimaryLoading}
	      variant="primary"
	      onClick={handleClick}
				isDisabled={isDisabled}	
	      {...extraPrimaryProps}
	    >
	      {spawningStatus}
	    </Button>
	  </React.Fragment>
	);
};

ButtonProgressVariants.propTypes = {
	clickCallback: PropTypes.func
}

const NewServerForm: React.FunctionComponent = function(props) {
	const {
		profileList
	} = props;
	let styleServerNameError = { color : '--pf-global--palette--red-100' } as React.CSSProperties;
	const [profileName, setProfileName] = useState('');
	const [serverName, setServerName] = useState('');
	const [userName, setUserName] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [serverNameError, setServerNameError] = useState('');
	const [spawningStatus, setSpawningStatus] = useState('Create');
	const [redirectSpawning, setRedirectSpawning] = useState(false);

	const updateProfileCallback = function(profile) {
		setProfileName(profile);
	}

	const handleServerNameChange = function(name) {
		const re = /\s/;
		const hasSpace = re.exec(name);
		if (hasSpace !== null) {
			setServerNameError("Server name must not contain space(s)");	
		} else {
			setServerNameError("");	
		}
		setServerName(name);
	}

	const formSubmitCallback = function(setLoadingStatus) {
		// POST API to spawn new server here
		getWhoAmI()
		.then(userModel => userModel.name)
		.then(_userName => {
			setUserName(_userName);
			return spawnNewserver(_userName, serverName, profileName)
		})
		.then(res => {
			console.log("Response when creating new server:", res)
			setSpawningStatus("Spawning");
			setRedirectSpawning(true);
		})
		.catch(error => {
			// TODO: Add more detail error message here
			setErrorMessage(error.message);
			console.error('There was an error!', error);
			setLoadingStatus(false);
			setSpawningStatus("Error")
		});
	}
	return (
	<Grid>
			<GridItem span={8}>
				<Form>
					<FormGroup
						label="Notebook server name"
						isRequired
						fieldId="notebook-form-name-01"
						helperText="Your notebook server name. Must be unique"
					>
						<TextInput
							isRequired
							type="text"
							id="notebook-form-name-01"
							name="notebook-form-name-01"
							aria-describedby="notebook-form-name-01-helper"
							value={serverName}
							onChange={handleServerNameChange}
						/>
						{serverNameError === '' ? null : <Text className="server-err-msg" component="p">{serverNameError}</Text>}
					</FormGroup>
					<FormGroup
						label="Notebook server profile"
						isRequired
						fieldId="notebook-form-profile-01"
						helperText="Choose the spec of your notebook server"
					>
						<ServerProfileRadio 
							profileList={profileList}
							updateProfileCallback={updateProfileCallback}
						/>
					</FormGroup>
				</Form>
				<br></br>
				<GridItem span={2}>
					<ButtonProgressVariants 
						onClickFunc={formSubmitCallback} 
						spawningStatus={spawningStatus}
						isDisabled={serverNameError !== '' ? true : false}
					/>
				</GridItem>
				<GridItem span={4}>
						{errorMessage === '' ? null : <Text>{errorMessage}</Text>}
						{redirectSpawning ? <Redirect to = {normalizeRoute(`/spawn/${userName}/${encodeURIComponent(serverName)}`)} /> : null}
				</GridItem>	
			</GridItem>
	</Grid>
	);
}

NewServerForm.propTypes = {
	profileList: PropTypes.array
}

const NewServer: React.FunctionComponent = function(props) {
	const [list, setList] = useState([]);
	useEffect(() => {
		let mounted = true;
		getWhoAmI()
		  .then(items => {
		    if(mounted) {
		      setList(items.profile_list);
		    }
		  })
		return () => mounted = false;
	      }, [])
	return (
	<div>
		<PageSection variant={PageSectionVariants.light}>
			<TextContent>
				<Text component="h1">Create a new notebook server</Text>
			</TextContent>
			
		</PageSection>
		<PageSection>
			<NewServerForm	profileList={list}/>
		</PageSection>
	</div>
	)
}

export { NewServer };
