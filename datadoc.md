# Json-Event

Description of the JSON format containing an LHCb Event

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**EventNumber**|`number`|Identifies an event within a certain run. In combination with RunNumber a unique identifier.| :white_check_mark: Yes|
|**RunNumber**|`number`|Identifies a specifc run. In combination with EventNumber a unique identifier.| :white_check_mark: Yes|
|**MCParticles**|`object`|Dictionary(key:MCparticle) containing all MCParticles of this Event| :white_check_mark: Yes|
|**MCVertices**|`object`|Dictionary Key:MCVertex containing all MC primary vertices| :white_check_mark: Yes|
|**VPClusters**|`object`|Dictionary Key:VPCluster containing all clusters in the VELO| :white_check_mark: Yes|
|**VeloTracks**|`object`|Dictionary Key:VELO-track containing all reconstructed VELO tracks| :white_check_mark: Yes|


Additional properties are not allowed.

## .EventNumber :white_check_mark: 

Identifies an event within a certain run. In combination with RunNumber a unique identifier.

* **Type**: `number`
* **Required**: Yes

## .RunNumber :white_check_mark: 

Identifies a specifc run. In combination with EventNumber a unique identifier.

* **Type**: `number`
* **Required**: Yes

## .MCParticles :white_check_mark: 

Dictionary(key:MCparticle) containing all MCParticles of this Event

* **Type**: `object`
* **Required**: Yes

**Properties**

|  Key |Type|Description|Required|
|---|----|-----------|--------|
|**`^\d*$`**|`object`|Object represents MCParticles|No|


Additional properties are not allowed.


### .MCParticles.`^\d*$`

Object represents MCParticles

* **Type**: `object`
* **Required**: No

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**ClosestToBeam**|`number[6]`|The state(x,y,z,tx,tz,q/p) at which the MCParticle trajectory came closest to the beam.|No|
|**OVPos**|`number[3]`|The position (x,y,z) of the origin vertex of the MCParticle|No|
|**PV**|`string`|The key of the associated primary vertex of the MCParticle|No|
|**eta**|`number`|Eta of the MCParticle based on origin momentum vector|No|
|**fourMom**|`number[4]`|MCParticle 4-Momentum vector at its origin vertex|No|
|**isE**|`boolean`|True if MCParticle is electron|No|
|**islong**|`boolean`|True if MCParticle isvelo and has hits in the SciFi detector|No|
|**ispv**|`boolean`|True if MCParticle is coming from a primary vertex|No|
|**isvelo**|`boolean`|True if MCParticle has >= 3 hits in the VELO|No|
|**key**|`string`|Unique identifier within event, and used as key in the dictionary of MCParticles|No|


Additional properties are not allowed.

#### .MCParticles.`^\d*$`.ClosestToBeam

The state(x,y,z,tx,tz,q/p) at which the MCParticle trajectory came closest to the beam.

* **Type**: `number[6]`
* **Required**: No

#### .MCParticles.`^\d*$`.OVPos

The position (x,y,z) of the origin vertex of the MCParticle

* **Type**: `number[3]`
* **Required**: No

#### .MCParticles.`^\d*$`.PV

The key of the associated primary vertex of the MCParticle

* **Type**: `string`
* **Required**: No

#### .MCParticles.`^\d*$`.eta

Eta of the MCParticle based on origin momentum vector

* **Type**: `number`
* **Required**: No

#### .MCParticles.`^\d*$`.fourMom

MCParticle 4-Momentum vector at its origin vertex

* **Type**: `number[4]`
* **Required**: No

#### .MCParticles.`^\d*$`.isE

True if MCParticle is electron

* **Type**: `boolean`
* **Required**: No

#### .MCParticles.`^\d*$`.islong

True if MCParticle isvelo and has hits in the SciFi detector

* **Type**: `boolean`
* **Required**: No

#### .MCParticles.`^\d*$`.ispv

True if MCParticle is coming from a primary vertex

* **Type**: `boolean`
* **Required**: No

#### .MCParticles.`^\d*$`.isvelo

True if MCParticle has >= 3 hits in the VELO

* **Type**: `boolean`
* **Required**: No

#### .MCParticles.`^\d*$`.key

Unique identifier within event, and used as key in the dictionary of MCParticles

* **Type**: `string`
* **Required**: No




## .MCVertices :white_check_mark: 

Dictionary Key:MCVertex containing all MC primary vertices

* **Type**: `object`
* **Required**: Yes

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**`^\d*$`**|`object`|Object representing a MCVertex|No|


Additional properties are not allowed.


### .MCVertices.`^\d*$`

Object representing a MCVertex

* **Type**: `object`
* **Required**: No

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**Pos**|`number[3]`|Position (x,y,z) of primary vertex|No|
|**products**|`integer`|number of decay products|No|
|**key**|`string`|Unique identifier within event, and used as key in the dictionary of MCVertices|No|


Additional properties are not allowed.

#### .MCVertices.`^\d*$`.Pos

Position (x,y,z) of primary vertex

* **Type**: `number[3]`
* **Required**: No

#### .MCVertices.`^\d*$`.products

number of decay products

* **Type**: `integer`
* **Required**: No
* **Minimum**: ` >= 0`

#### .MCVertices.`^\d*$`.key

Unique identifier within event, and used as key in the dictionary of MCVertices

* **Type**: `string`
* **Required**: No




## .VPClusters :white_check_mark: 

Dictionary Key:VPCluster containing all clusters in the VELO

* **Type**: `object`
* **Required**: Yes

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**`^\d*$`**|`object`|Object representing a single VPCluster|No|


Additional properties are not allowed.


### .VPClusters.`^\d*$`

Object representing a single VPCluster

* **Type**: `object`
* **Required**: No

**Properties**

|Key   |Type|Description|Required|
|---|----|-----------|--------|
|**MCPs**|`string[]`|List of keys of associated MCParticles|No|
|**x**|`number`|X-position of VELO hit|No|
|**y**|`number`|Y-position of VELO hit|No|
|**z**|`number`|Z-position of VELO hit|No|
|**key**|`string`|Unique identifier within event, and used as key in the dictionary of VPClusters|No|


Additional properties are not allowed.

#### .VPClusters.`^\d*$`.MCPs

List of keys of associated MCParticles

* **Type**: `string[]`
* **Required**: No

#### .VPClusters.`^\d*$`.x

X-position of VELO hit

* **Type**: `number`
* **Required**: No

#### .VPClusters.`^\d*$`.y

Y-position of VELO hit

* **Type**: `number`
* **Required**: No

#### .VPClusters.`^\d*$`.z

Z-position of VELO hit

* **Type**: `number`
* **Required**: No

#### .VPClusters.`^\d*$`.key

Unique identifier within event, and used as key in the dictionary of VPClusters

* **Type**: `string`
* **Required**: No




## .VeloTracks :white_check_mark: 

Dictionary Key:VELO-track containing all reconstructed VELO tracks

* **Type**: `object`
* **Required**: Yes

**Properties**

|Key|Type|Description|Required|
|---|----|-----------|--------|
|**`^\d*$`**|`object`||No|


Additional properties are not allowed.


### .VeloTracks.`^\d*$`

* **Type**: `object`
* **Required**: No

**Properties**

| Key  |Type|Description|Required|
|---|----|-----------|--------|
|**ClosestToBeam**|`number[6]`|The state(x,y,z,tx,tz,q/p) at which the (extrapolated) track came closest to the beam.|No|
|**LHCbIDs**|`string[3-*]`|List of keys of VPClusters(hits) used to reconstruct this track|No|
|**MCPs**|`string[]`|List of keys of associated MCParticles|No|
|**errCTBState**|`number[5]`|Covariance matrix of closest to beam state. Only non-zero elements (x,y,tx,ty, Cov(x,tx)). Cov(x,tx)= Cov(x,ty)= Cov(y,tx)= Cov(y,ty)|No|
|**isBackwards**|`boolean`|True if tracks momentum points into backwards direction|No|
|**key**|`string`|Unique identifier within event, and used as key in the dictionary of VELO-tracks|No|


Additional properties are not allowed.

#### .VeloTracks.`^\d*$`.ClosestToBeam

The state(x,y,z,tx,tz,q/p) at which the (extrapolated) track came closest to the beam.

* **Type**: `number[6]`
* **Required**: No

#### .VeloTracks.`^\d*$`.LHCbIDs

List of keys of VPClusters(hits) used to reconstruct this track

* **Type**: `string[3-*]`
* **Required**: No

#### .VeloTracks.`^\d*$`.MCPs

List of keys of associated MCParticles

* **Type**: `string[]`
* **Required**: No

#### .VeloTracks.`^\d*$`.errCTBState

Covariance matrix of closest to beam state. Only non-zero elements (x,y,tx,ty, Cov(x,tx)). Cov(x,tx)= Cov(x,ty)= Cov(y,tx)= Cov(y,ty)

* **Type**: `number[5]`
* **Required**: No

#### .VeloTracks.`^\d*$`.isBackwards

True if tracks momentum points into backwards direction

* **Type**: `boolean`
* **Required**: No

#### .VeloTracks.`^\d*$`.key

Unique identifier within event, and used as key in the dictionary of VELO-tracks

* **Type**: `string`
* **Required**: No





